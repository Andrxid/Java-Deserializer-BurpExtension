# JavaDeserializer - Burp Suite Extension

JavaDeserializer is a Burp Suite extension that allows you to view Java serialized payloads in JSON format.

## Features

- Automatically detects Java serialized payloads in HTTP requests and responses
- Deserializes content and displays it in formatted JSON
- Supports viewing in both requests and responses
- Simple and intuitive interface integrated into Burp Suite

## Installation

1. Download the latest version of Jython Standalone JAR
2. In Burp Suite, go to `Extender` -> `Options`
3. Under "Python Environment", configure the path to Jython Standalone JAR
4. Go to the `Extensions` tab and click `Add`
5. Select `Python` as the extension type
6. Select the `deserializerjava.py` file
7. Click `Next` to complete the installation

## Usage

Once installed, the extension adds a new tab called "Java Deserialize" in Burp Suite's request/response inspection panel.

When a Java serialized payload is intercepted:
1. The "Java Deserialize" tab will automatically activate
2. The serialized content will be deserialized and shown in JSON format
3. The JSON will be prettified for better readability

## Requirements

- Burp Suite Professional or Community
- Jython Standalone 2.7.x
- Java Runtime Environment (JRE) 8 or higher

## Limitations

- The extension is read-only and does not allow payload modification
- Only supports standard Java serialized payloads
- Errors may occur with malformed payloads or non-standard Java classes

## License

This project is distributed under the MIT License. See the `LICENSE` file for more details.

## Contributing

Contributions are welcome! If you want to contribute:
1. Fork the repository
2. Create a branch for your changes
3. Submit a pull request

## Issue Reporting

If you encounter any issues or have suggestions, please open a GitHub issue describing:
- Expected behavior
- Actual behavior
- Steps to reproduce the issue
- Any error logs