from fpdf import FPDF
import os
from datetime import datetime

def pdf_for_model_performance(data, filepath):
    
    historical_data_plot_path = data["historical_data_plot_path"]
    forecast_data_plot_path = data["forecast_data_plot_path"]

    class PDF(FPDF):
        pass

    mx = 15
    my = 15

    pdf = PDF('P', 'mm', 'Letter')
    pdf.set_auto_page_break(True, margin=5)
    pdf.add_font("tinos-regular", style="", fname=os.path.join(os.path.dirname(__file__), "../static/Tinos-Regular.ttf"))
    pdf.add_font("tinos-regular", style="B", fname=os.path.join(os.path.dirname(__file__), "../static/Tinos-Bold.ttf"))
    pdf.set_font(family='tinos-regular')

    pdf.add_page()

    plot_image_ratio = 1.8333
    gap_between_text_and_image = 5
    gap_between_two_plots = 10

    x, y = mx, my+5

    pdf.set_font(size=20, style='B')
    pdf.text(x=x, y=y, text="Results of Linear regression prediction")

    pdf.set_font(size=12)
    x, y = x, y+20
    pdf.text(x=x, y=y, text="Plot for the comparison of predicted and actual prices of 25th day into the future")
    w, h, x, y = plot_image_ratio*80, 80, x, y + gap_between_text_and_image
    pdf.image(historical_data_plot_path, w=w, h=h, x=x, y=y)

    x, y = x, y + h + gap_between_two_plots
    pdf.text(x=x, y=y, text="Plot for comparing 30 days of prediction")
    w, h, x, y = w, h, x, y + gap_between_text_and_image
    pdf.image( forecast_data_plot_path, w=w, h=h, x=x, y=y)

    # pdf.add_page()
    # x, y = mx, my+5
    # pdf.text(x=x, y=y, text="Plot for comparing prediction of only 30days into the future")
    # w, h, x, y = w, h, x, y + gap_between_text_and_image
    # pdf.image('gg.png', w=w, h=h, x=x, y=y)

    pdf.output(filepath)


def pdf_for_backtest(data, filepath):
    
    class PDF(FPDF):
        pass

    mx = 15
    my = 15

    pdf = PDF('P', 'mm', 'Letter')
    pdf.set_auto_page_break(True, margin=5)
    pdf.add_font("tinos-regular", style="", fname=os.path.join(os.path.dirname(__file__), "../static/Tinos-Regular.ttf"))
    pdf.add_font("tinos-regular", style="B", fname=os.path.join(os.path.dirname(__file__), "../static/Tinos-Bold.ttf"))
    pdf.set_font(family='tinos-regular')

    pdf.add_page()

    plot_image_ratio = 1.8333
    gap_between_text_and_image = 5
    gap_between_two_plots = 10

    x, y = mx, my+5

    pdf.set_font(size=20, style='B')
    pdf.text(x=x, y=y, text="Result of backtest")
    y += 5
    pdf.set_font(size=10)
    pdf.text(x=x, y=y, text=datetime.strftime(data["issue_date"], "%Y-%m-%d"))

    pdf.set_font(size=12, style='B')
    x, y = x, y+20
    pdf.text(x=x, y=y, text="Financial metrics")
    y += 5
    pdf.set_font(size=12, style='')
    for metric in ["sharpe", "sortino", "VaR", "max_drawdown", "trade_count", "total_return"]:
        x, y = x, y+5
        pdf.text(x=x, y=y, text=metric.replace('_',' ').title())
        pdf.text(x=x+35, y=y, text="{:.4f}".format(data[metric]))

    x, y = x, y + 20
    pdf.set_font(size=12, style='B')
    pdf.text(x=x, y=y, text="Plot of returns over backtesting period")
    w, h, x, y = plot_image_ratio*80, 80, x, y + 5
    pdf.image( data["returns_plot_filepath"], w=w, h=h, x=x, y=y)

    pdf.output(filepath)
    
    

def pdf_for_forecast(data, filepath):
    
    class PDF(FPDF):
        pass

    mx = 15
    my = 15

    pdf = PDF('P', 'mm', 'Letter')
    pdf.set_auto_page_break(True, margin=5)
    pdf.add_font("tinos-regular", style="", fname=os.path.join(os.path.dirname(__file__), "../static/Tinos-Regular.ttf"))
    pdf.add_font("tinos-regular", style="B", fname=os.path.join(os.path.dirname(__file__), "../static/Tinos-Bold.ttf"))
    pdf.set_font(family='tinos-regular')

    pdf.add_page()

    plot_image_ratio = 1.8333
    gap_between_text_and_image = 5
    gap_between_two_plots = 10

    x, y = mx, my+5

    pdf.set_font(size=20, style='B')
    pdf.text(x=x, y=y, text="Forecast result")
    y += 5
    pdf.set_font(size=10)
    pdf.text(x=x, y=y, text=datetime.strftime(data["start_date"], "%Y-%m-%d"))

    w, h, x, y = plot_image_ratio*80, 80, x, y + 20
    pdf.image( data["forecast_plot_filepath"], w=w, h=h, x=x, y=y)

    pdf.output(filepath)