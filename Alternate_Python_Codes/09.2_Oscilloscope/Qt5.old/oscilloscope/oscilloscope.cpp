#include "oscilloscope.h"
#include "ui_oscilloscope.h"

Oscilloscope::Oscilloscope(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::Oscilloscope)
{
    ui->setupUi(this);
}

Oscilloscope::~Oscilloscope()
{
    delete ui;
}

