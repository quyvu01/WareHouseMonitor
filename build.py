"""
Script để đóng gói ứng dụng Warehouse Temperature Monitor thành ứng dụng độc lập.
Sử dụng PyInstaller để tạo ra file thực thi.
"""

import os
import sys
import subprocess
import shutil

def build_standalone_app():
    """Đóng gói ứng dụng thành file thực thi độc lập"""
    print("Bắt đầu đóng gói ứng dụng...")
    
    # Kiểm tra PyInstaller đã được cài đặt chưa
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller đã được cài đặt thành công.")
    except subprocess.CalledProcessError:
        print("Không thể cài đặt PyInstaller. Vui lòng cài đặt thủ công: pip install pyinstaller")
        return False
    
    # Tạo file khởi động ứng dụng
    with open("run_app.py", "w") as f:
        f.write("""
import subprocess
import os
import sys
import webbrowser
import time
import signal
import platform

def run_streamlit():
    print("Đang khởi động Warehouse Temperature Monitor...")
    
    # Đường dẫn đến Streamlit
    streamlit_cmd = os.path.join(os.path.dirname(sys.executable), "streamlit")
    if platform.system() == "Windows":
        streamlit_cmd += ".exe"
    
    # Khởi động Streamlit
    process = subprocess.Popen(
        [streamlit_cmd, "run", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Đợi cho ứng dụng khởi động
    time.sleep(3)
    
    # Mở trình duyệt
    webbrowser.open("http://localhost:8501")
    
    # Xử lý tín hiệu để tắt ứng dụng khi người dùng nhấn Ctrl+C
    def signal_handler(sig, frame):
        print("\\nĐang tắt ứng dụng...")
        process.terminate()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Hiển thị output từ Streamlit
    print("Ứng dụng đang chạy. Nhấn Ctrl+C để tắt.")
    try:
        while True:
            output = process.stdout.readline()
            if output:
                print(output.strip())
            
            error = process.stderr.readline()
            if error:
                print(f"Lỗi: {error.strip()}", file=sys.stderr)
            
            if process.poll() is not None:
                break
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\\nĐang tắt ứng dụng...")
        process.terminate()

if __name__ == "__main__":
    run_streamlit()
""")
    
    # Xây dựng file thực thi bằng PyInstaller
    try:
        subprocess.run([
            "pyinstaller",
            "--name=WarehouseTemperatureMonitor",
            "--onefile",
            "--windowed",
            "--add-data=app.py:.",
            "--add-data=anomaly_detection.py:.",
            "--add-data=database.py:.",
            "--add-data=mock_data.py:.",
            "--add-data=sensor.py:.",
            "--add-data=utils.py:.",
            "--add-data=visualization.py:.",
            "--icon=generated-icon.png",
            "run_app.py"
        ], check=True)
        
        print("Đóng gói thành công!")
        print("File thực thi được lưu tại: dist/WarehouseTemperatureMonitor")
        
        # Sao chép các file cần thiết khác
        shutil.copy("warehouse_temperature.db", "dist/")
        
        # Tạo file README cho phiên bản độc lập
        with open("dist/README.txt", "w", encoding="utf-8") as f:
            f.write("""
Warehouse Temperature Monitor
============================

Hướng dẫn sử dụng:
1. Chạy file WarehouseTemperatureMonitor
2. Ứng dụng sẽ tự động mở trong trình duyệt web của bạn
3. Nếu trình duyệt không tự động mở, hãy truy cập vào địa chỉ: http://localhost:8501

Lưu ý: Khi bạn đóng cửa sổ terminal, ứng dụng sẽ tự động tắt.
""")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi đóng gói ứng dụng: {e}")
        return False

if __name__ == "__main__":
    if build_standalone_app():
        print("Quá trình đóng gói hoàn tất!")
    else:
        print("Quá trình đóng gói thất bại!")