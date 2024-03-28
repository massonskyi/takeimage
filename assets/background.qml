import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: "Gradient Background Animation"

    Rectangle {
        id: backgroundRect
        anchors.fill: parent
        color: "transparent"

        // Градиентный фон
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#282a36" } // Начальный цвет фона
            GradientStop { position: 1.0; color: "#6272a4" } // Конечный цвет фона
        }

        // Анимация для переплывающего фона
        SequentialAnimation on opacity {
            loops: Animation.Infinite
            NumberAnimation { from: 0.0; to: 1.0; duration: 5000 } // Анимация смены цвета от прозрачного к непрозрачному
            PauseAnimation { duration: 1000 } // Пауза между сменами цвета
            NumberAnimation { from: 1.0; to: 0.0; duration: 5000 } // Анимация смены цвета от непрозрачного к прозрачному
        }
    }

    ColumnLayout {
        anchors.centerIn: parent

        Text {
            text: "Hello, World!"
            font.pixelSize: 24
            color: "white"
        }

        Button {
            text: "Click me!"
        }
    }