import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    visible: true
    width: 600
    height: 400
    title: qsTr("Text to Image Converter")

    ImageConverter {
        id: imageConverter
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        Text {
            text: "Enter Text:"
        }
        TextArea {
            id: inputText
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        Text {
            text: "Select Style:"
        }
        ComboBox {
            id: styleCombo
            Layout.fillWidth: true
            model: styleModel
            textRole: "title"
        }

        Text {
            text: "Number of Images:"
        }
        SpinBox {
            id: countRequestSpin
            from: 1
            to: 4
            value: 1
        }

        Button {
            text: "Convert"
            onClicked: convertTextToImage()
        }

        Repeater {
            model: imageModel
            delegate: Image {
                source: "data:image/jpeg;base64," + modelData
                width: 200
                height: 200
            }
        }
    }

    ListModel {
        id: styleModel
    }

    ListModel {
        id: imageModel
    }

    Component.onCompleted: {
        // Populate style combo box
        populateStyles()
    }

    function populateStyles() {
        styleModel.clear()
        var styles = imageConverter.getStyles()
        for (var i = 0; i < styles.length; ++i) {
            styleModel.append({ "title": styles[i].title })
        }
    }

    function convertTextToImage() {
        var text = inputText.text
        var styleIndex = styleCombo.currentIndex
        var style = styleModel.get(styleIndex).title
        var countRequest = countRequestSpin.value

        // Call Python function here passing text, style, and countRequest
        var imagesBase64 = imageConverter.convertTextToImage(text, style, countRequest)
        imageModel.clear()
        for (var i = 0; i < imagesBase64.length; ++i) {
            imageModel.append({ "image": imagesBase64[i] })
        }
    }
}