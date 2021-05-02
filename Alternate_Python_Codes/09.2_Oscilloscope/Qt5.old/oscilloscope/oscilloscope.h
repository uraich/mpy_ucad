#ifndef OSCILLOSCOPE_H
#define OSCILLOSCOPE_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class Oscilloscope; }
QT_END_NAMESPACE

class Oscilloscope : public QMainWindow
{
    Q_OBJECT

public:
    Oscilloscope(QWidget *parent = nullptr);
    ~Oscilloscope();

private:
    Ui::Oscilloscope *ui;
};
#endif // OSCILLOSCOPE_H
