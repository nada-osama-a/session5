pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Shapes

Rectangle {
    id: root
    width: 300
    height: 300
    color: palette.window

    required property var dataClass

    property real myAngle: dataClass.angle
    
    Rectangle {
        id: myCircle
        anchors.centerIn: root
        width: (parent.width > parent.height) ? parent.height : parent.width
        height: width
        radius: width / 2
        border.width: 12
        border.color: '#555555'
        color: (palette.window.hsvValue > 0.5) ? 'black' : 'white'

        Repeater {
            model: 36

            delegate: Item {
                id: tickContainer

                required property int index

                anchors.bottom: myCircle.verticalCenter
                anchors.topMargin: 16
                anchors.top: myCircle.top
                anchors.horizontalCenter: parent.horizontalCenter

                rotation: index * 10
                transformOrigin: Item.Bottom

                Rectangle {
                    width: 2
                    height: 10
                    color: (palette.window.hsvValue > 0.5) ? 'white' : 'black'
                    anchors.top: parent.top
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Text {
                    color: (palette.window.hsvValue > 0.5) ? 'white' : 'black'
                    text: (parent.index*10 %90) ? '' : parent.index*10
                    font.pixelSize: 16
                    font.bold: true

                    anchors.topMargin: 16
                    anchors.top: parent.top
                    anchors.horizontalCenter: parent.horizontalCenter
                    rotation: -parent.rotation
                }
            }
        }

        Shape{
            id: pointer
            anchors.topMargin: parent.height * 0.1
            anchors.top: parent.top
            anchors.bottom: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width * 0.04
            rotation: root.myAngle
            transformOrigin: Item.Bottom

            ShapePath {
                strokeColor: 'red'
                strokeWidth: 1
                fillColor: 'red'

                startX: 0
                startY: pointer.height

                PathLine{x: pointer.width / 2; y: 0}
                PathLine{x: pointer.width; y: pointer.height}
                PathLine{x: 0; y: pointer.height}
            }
        }
    }
}