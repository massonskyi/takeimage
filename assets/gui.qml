import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 1280
    height: 800
    title: "Text to Image API"
    color: "#282a36"

    Rectangle {
        id: content
        anchors.fill: parent

        ColumnLayout {
            anchors.centerIn: parent
            spacing: 10

            Label {
                text: "Text:"
                color: "#f8f8f2"
            }
            TextField {
                placeholderText: "Enter text"
                color: "#f8f8f2"
                background: Rectangle {
                    color: "#44475a"
                    border.color: content.focus ? "#6272a4" : "#44475a"
                    radius: 5
                }
                focus: true
            }

            Label {
                text: "Negative:"
                color: "#f8f8f2"
            }
            TextField {
                placeholderText: "Enter negative (optional)"
                color: "#f8f8f2"
                background: Rectangle {
                    color: "#44475a"
                    border.color: content.focus ? "#6272a4" : "#44475a"
                    radius: 5
                }
            }

            Label {
                text: "Style:"
                color: "#f8f8f2"
            }
            ComboBox {
                color: "#f8f8f2"
                background: Rectangle {
                    color: "#44475a"
                    border.color: content.focus ? "#6272a4" : "#44475a"
                    radius: 5
                }
                model: styleModel
                currentIndex: 0
            }

            Label {
                text: "Count:"
                color: "#f8f8f2"
            }
            SpinBox {
                color: "#f8f8f2"
                background: Rectangle {
                    color: "#44475a"
                    border.color: content.focus ? "#6272a4" : "#44475a"
                    radius: 5
                }
                from: 1
                to: 10
                value: 1
            }

            Button {
                text: "Generate Images"
                color: "#f8f8f2"
                background: Rectangle {
                    color: "#6272a4"
                    border.color: content.pressed ? "#44475a" : "#6272a4"
                    radius: 5
                }
                hoverEnabled: true
                onClicked: {}
            }

            ScrollArea {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Rectangle {
                    width: content.width - 20
                    height: content.height - 20
                    color: "#282a36"
                }
            }
        }
    }

    StatusBar {
        RowLayout {
            Layout.alignment: Qt.AlignRight

            Label {
                text: "Copyright © 2023 massonskyi"
                color: "#abb2bf"
            }
        }
    }

    ListModel {
        id: styleModel
        ListElement { name: "Style 1" }
        ListElement { name: "Style 2" }
        // Add more styles as needed
    }
}