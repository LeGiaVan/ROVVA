from flask import Blueprint, render_template

report_bp = Blueprint("report", __name__, url_prefix="/reports")

@report_bp.route("/")
def index():
    # Mock data for demonstration
    stats = {
        'revenue': {'value': '125.000.000đ', 'trend': '+ 12%'},
        'bookings': {'value': '348', 'trend': '+ 8%'},
        'occupancy': {'value': '82%', 'trend': '+ 8%'},
        'cancellation': {'value': '6%', 'trend': '- 2%'},
        'nights': {'value': '1.245', 'label': 'đêm'}
    }
    
    # Bar chart mock data
    bar_chart_data = [65, 80, 50, 95, 110, 150, 120, 90, 130, 115, 140, 10]
    
    # Table mock data - CSLT
    accommodations_perf = [
        {'name': 'Homestay Đà Lạt View', 'bookings': 145, 'revenue': '52.400.000đ', 'occupancy': 88},
        {'name': 'Villa Biển Vũng Tàu', 'bookings': 92, 'revenue': '48.200.000đ', 'occupancy': 76},
        {'name': 'Vinhomes Central', 'bookings': 111, 'revenue': '24.400.000đ', 'occupancy': 82}
    ]
    
    # Table mock data - Phòng
    rooms_perf = [
        {'name': 'Phòng 101', 'acc': 'Đà Lạt View', 'revenue': '12.500.000đ', 'occupancy': '10%'},
        {'name': 'Phòng 202', 'acc': 'Đà Lạt View', 'revenue': '11.800.000đ', 'occupancy': '9.4%'},
        {'name': 'Nguyên căn', 'acc': 'Villa Vũng Tàu', 'revenue': '48.200.000đ', 'occupancy': '38.5%'}
    ]
    
    # Table mock data - Chi tiết doanh thu
    transactions = [
        {'date': '12/10/2024', 'acc': 'Homestay Đà Lạt View', 'room': 'Phòng 101', 'code': '#RV-9921', 'revenue': '1.200.000đ', 'status': 'Thành công', 'status_color': 'success'},
        {'date': '12/10/2024', 'acc': 'Villa Biển Vũng Tàu', 'room': 'Nguyên căn', 'code': '#RV-9918', 'revenue': '5.500.000đ', 'status': 'Thành công', 'status_color': 'success'},
        {'date': '11/10/2024', 'acc': 'Vinhomes Central', 'room': 'Studio 402', 'code': '#RV-9855', 'revenue': '850.000đ', 'status': 'Đang ở', 'status_color': 'primary'},
        {'date': '10/10/2024', 'acc': 'Homestay Đà Lạt View', 'room': 'Phòng 202', 'code': '#RV-9840', 'revenue': '0đ', 'status': 'Hủy bỏ', 'status_color': 'danger'}
    ]

    return render_template(
        "host/report/index.html", 
        active_nav="reports",
        stats=stats,
        bar_chart_data=bar_chart_data,
        accommodations_perf=accommodations_perf,
        rooms_perf=rooms_perf,
        transactions=transactions
    )
