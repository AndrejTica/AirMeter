#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "CSV_read.h"

using namespace std;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_pushButton_clicked()
{
    CSVRead quelle("/home/andre/Airmeter/Standalone/chart/airMeter_20210202.csv");
    QLineSeries *series = new QLineSeries();
    vector<string> column = quelle.getColumn(4);
        int x=1;
        for (auto tokens : column)
            {
            x++;
            series->append(x, stod( tokens ));
            }



     // Create chart, add data, hide legend, and add axis
     QChart *chart = new QChart();
     chart->legend()->hide();
     chart->addSeries(series);
     chart->createDefaultAxes();

     // Customize the title font
     QFont font;
     font.setPixelSize(1);
     chart->setTitleFont(font);
     chart->setTitleBrush(QBrush(Qt::black));
     chart->setTitle("Airmeter");

     // Change the line color and weight
     QPen pen(QRgb(0x000000));
     pen.setWidth(1);
     series->setPen(pen);

     chart->setAnimationOptions(QChart::AllAnimations);

     // Change the x axis categories
     QCategoryAxis *axisX = new QCategoryAxis();
     vector<string> xAxis = quelle.getX_Axis();
       int y = 0;
         for (auto tokens : xAxis)
             {
             y++;
             axisX->append(QString::fromStdString(tokens),y);
             }
     axisX->setLabelsAngle(280);
     axisX->setTitleText("Sensor");
     chart->setAxisX(axisX, series);
     // Used to display the chart
     QChartView *chartView = new QChartView(chart);
     chartView->setRubberBand(QChartView::HorizontalRubberBand);
     chartView->setRenderHint(QPainter::Antialiasing);
     //chartView->setParent(ui->widgetGraph);
     setCentralWidget(chartView);
       // chartView->setParent(ui->widgetGraph);
}
