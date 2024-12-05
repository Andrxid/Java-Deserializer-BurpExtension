# -*- coding: utf-8 -*-

from burp import IBurpExtender, IMessageEditorTabFactory, IMessageEditorTab
from java.io import (
    ByteArrayInputStream,
    ObjectInputStream,
    PrintWriter,
)
from javax.swing import JPanel, JLabel, JScrollPane, JTextArea
from java.awt import BorderLayout
import traceback
from com.fasterxml.jackson.databind import ObjectMapper

class BurpExtender(IBurpExtender, IMessageEditorTabFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("JavaDeserializer")
        self._stdout = PrintWriter(callbacks.getStdout(), True)
        self._stderr = PrintWriter(callbacks.getStderr(), True)
        callbacks.registerMessageEditorTabFactory(self)
        self._stdout.println("Estensione 'Java Payload Deserializer Editable' caricata correttamente.")

    def createNewInstance(self, controller, editable):
        self._stdout.println("createNewInstance: Creazione di una nuova istanza di CustomTab.")
        return CustomTab(controller, editable, self._callbacks, self._helpers, self._stdout)

class CustomTab(IMessageEditorTab):
    def __init__(self, controller, editable, callbacks, helpers, stdout):
        self._editable = editable
        self._callbacks = callbacks
        self._helpers = helpers
        self._stdout = stdout
        self._controller = controller
        self._panel = JPanel(BorderLayout())
        self._label = JLabel("Contenuto deserializzato:")
        self._textArea = JTextArea("Nessun dato elaborato.")
        self._textArea.setLineWrap(True)
        self._textArea.setWrapStyleWord(True)
        self._textArea.setEditable(False)
        self._scrollPane = JScrollPane(self._textArea)
        
        self._panel.add(self._label, BorderLayout.NORTH)
        self._panel.add(self._scrollPane, BorderLayout.CENTER)

        self._currentMessage = None
        self._objectMapper = ObjectMapper()

    def getTabCaption(self):
        return "Java Deserialize"

    def getUiComponent(self):
        return self._panel

    def isEnabled(self, content, isRequest):
        if content is None:
            return False
        body = self._getBody(content, isRequest)
        return len(body) > 2 and (body[0] == -84 or body[0] & 0xFF == 0xAC) and (body[1] == -19 or body[1] & 0xFF == 0xED)

    def setMessage(self, content, isRequest):
        self._currentMessage = content
        if content is None:
            self._textArea.setText("Nessun dato disponibile.")
            return

        try:
            body = self._getBody(content, isRequest)
            byte_stream = ByteArrayInputStream(body)
            object_stream = ObjectInputStream(byte_stream)
            deserialized_object = object_stream.readObject()
            json_str = self._objectMapper.writerWithDefaultPrettyPrinter().writeValueAsString(deserialized_object)
            self._textArea.setText(json_str)
        except Exception as e:
            self._textArea.setText("Error during deserialization: {}".format(str(e)))
            self._stdout.println("setMessage: Error during deserialization: {}".format(str(e)))
            self._stdout.println(traceback.format_exc())

    def getMessage(self):
        return self._currentMessage

    def isModified(self):
        return False

    def getSelectedData(self):
        return None

    def _getBody(self, content, isRequest):
        info = self._helpers.analyzeRequest(content) if isRequest else self._helpers.analyzeResponse(content)
        return content[info.getBodyOffset():]
