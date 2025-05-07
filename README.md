# Hệ thống Theo dõi Nhiệt độ Kho hàng

Đây là ứng dụng giám sát nhiệt độ và độ ẩm của kho hàng, có khả năng phát hiện bất thường và hiển thị dữ liệu theo thời gian thực.

## Tính năng chính

- Theo dõi nhiệt độ và độ ẩm theo thời gian thực 
- Hiển thị biểu đồ dữ liệu lịch sử
- Phát hiện bất thường tự động
- Hỗ trợ kết nối với cảm biến qua cổng serial
- Lưu trữ dữ liệu vào cơ sở dữ liệu SQLite
- Xuất dữ liệu dưới dạng CSV

## Cài đặt

1. Cài đặt Python (phiên bản 3.8 trở lên)
2. Tải về mã nguồn
3. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

Để chạy ứng dụng, sử dụng lệnh:

```bash
streamlit run app.py
```

Ứng dụng sẽ tự động mở trong trình duyệt web mặc định của bạn. Nếu không, bạn có thể truy cập tại địa chỉ http://localhost:8501

## Kết nối với cảm biến

Ứng dụng này hỗ trợ đọc dữ liệu từ cảm biến kết nối qua cổng Serial. Cảm biến cần gửi dữ liệu theo định dạng:

```
Temperature: XX.X, Humidity: YY.Y
```

Nếu bạn chưa có cảm biến, ứng dụng cũng hỗ trợ tạo dữ liệu mẫu để kiểm thử.

## Cấu hình

Các thông số cấu hình có thể được điều chỉnh trong giao diện người dùng:

- Ngưỡng phát hiện bất thường
- Ngưỡng cảnh báo nhiệt độ và độ ẩm 
- Khung thời gian hiển thị dữ liệu lịch sử
- Cổng Serial và tốc độ baud khi kết nối với cảm biến thực

## Yêu cầu hệ thống

- Python 3.8 hoặc cao hơn
- Các thư viện Python: streamlit, pandas, numpy, matplotlib, plotly, scikit-learn, pyserial
- Tối thiểu 2GB RAM
- Khoảng 100MB dung lượng ổ đĩa