# Hướng dẫn Cài đặt Hệ thống Theo dõi Nhiệt độ Kho hàng

## Cài đặt trên Windows

### Cách 1: Cài đặt từ mã nguồn (cần cài Python)

1. Cài đặt Python từ [trang chủ Python](https://www.python.org/downloads/windows/):
   - Chọn phiên bản Python 3.8 hoặc cao hơn
   - Khi cài đặt, đánh dấu vào "Add Python to PATH"

2. Tải về và giải nén mã nguồn ứng dụng

3. Mở Command Prompt và chuyển đến thư mục vừa giải nén:
   ```
   cd đường-dẫn-đến-thư-mục
   ```

4. Cài đặt các thư viện cần thiết:
   ```
   pip install -r dependencies.txt
   ```

5. Chạy ứng dụng:
   ```
   streamlit run app.py
   ```

### Cách 2: Sử dụng phiên bản đóng gói (không cần cài Python)

1. Tải về file WarehouseTemperatureMonitor.exe từ [trang tải xuống](https://example.com/download)

2. Chạy file WarehouseTemperatureMonitor.exe
   - Ứng dụng sẽ tự động mở trong trình duyệt web của bạn
   - Nếu trình duyệt không tự mở, truy cập địa chỉ: http://localhost:8501

## Cài đặt trên macOS

### Cách 1: Cài đặt từ mã nguồn (cần cài Python)

1. Nếu chưa có, cài đặt Homebrew bằng cách mở Terminal và chạy:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Cài đặt Python:
   ```
   brew install python
   ```

3. Tải về và giải nén mã nguồn ứng dụng

4. Mở Terminal và chuyển đến thư mục vừa giải nén:
   ```
   cd đường-dẫn-đến-thư-mục
   ```

5. Cài đặt các thư viện cần thiết:
   ```
   pip3 install -r dependencies.txt
   ```

6. Chạy ứng dụng:
   ```
   streamlit run app.py
   ```

### Cách 2: Sử dụng phiên bản đóng gói (không cần cài Python)

1. Tải về file WarehouseTemperatureMonitor.dmg từ [trang tải xuống](https://example.com/download)

2. Mở file .dmg và kéo ứng dụng vào thư mục Applications

3. Chạy ứng dụng từ Launchpad hoặc thư mục Applications

## Cài đặt trên Linux

1. Cài đặt Python và pip (ví dụ trên Ubuntu):
   ```
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. Tải về và giải nén mã nguồn ứng dụng

3. Mở Terminal và chuyển đến thư mục vừa giải nén:
   ```
   cd đường-dẫn-đến-thư-mục
   ```

4. Cài đặt các thư viện cần thiết:
   ```
   pip3 install -r dependencies.txt
   ```

5. Chạy ứng dụng:
   ```
   streamlit run app.py
   ```

## Kết nối với cảm biến thực

### Windows
- Cài đặt driver cho thiết bị USB-to-Serial nếu bạn đang sử dụng adapter.
- Cổng COM thường có dạng COM1, COM2, v.v. và có thể tìm thấy trong Device Manager.

### macOS
- Cổng serial thường có dạng `/dev/tty.usbserial-*` hoặc `/dev/tty.usbmodem*`.
- Bạn có thể tìm chúng bằng lệnh: `ls /dev/tty.*` trong Terminal.

### Linux
- Cổng serial thường có dạng `/dev/ttyUSB0` hoặc `/dev/ttyACM0`.
- Bạn có thể tìm chúng bằng lệnh: `ls /dev/tty*` trong Terminal.
- Đảm bảo người dùng có quyền truy cập vào thiết bị serial:
  ```
  sudo usermod -a -G dialout $USER
  ```
  (Cần đăng xuất và đăng nhập lại để có hiệu lực)

## Xử lý sự cố kết nối 

Nếu bạn gặp vấn đề khi kết nối với cảm biến, hãy thử:

1. Kiểm tra lại cổng kết nối và tốc độ baud trong cài đặt ứng dụng
2. Đảm bảo cảm biến đang hoạt động và được cấp đủ nguồn điện
3. Kiểm tra định dạng dữ liệu từ cảm biến (phải là `Temperature: XX.X, Humidity: YY.Y`)
4. Đảm bảo quyền truy cập vào cổng COM/Serial (đặc biệt trên Linux/macOS)

Nếu vẫn gặp vấn đề, bạn có thể dùng chế độ dữ liệu mẫu để kiểm tra các chức năng của ứng dụng.