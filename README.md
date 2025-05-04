 
## <span style="border-bottom: 2px solid #1DB954; padding-bottom: 3px;">Mục lục</span>

<div style="font-family: Arial, sans-serif; line-height: 1.8;">

1. <span style="border-bottom: 1px dashed #1DB954;">Tổng quan</span>  
2. <span style="border-bottom: 1px dashed #1DB954;">Công nghệ</span>  
3. <span style="border-bottom: 1px dashed #1DB954;">Yêu cầu hệ thống</span>  
4. <span style="border-bottom: 1px dashed #1DB954;">Cài đặt</span>  
   - <span style="border-bottom: 1px dotted #1DB954;">Biến môi trường</span>  
   - <span style="border-bottom: 1px dotted #1DB954;">Cấu hình database</span>  
<!--5. <span style="border-bottom: 1px dashed #1DB954;">API Endpoints</span>  
6. <span style="border-bottom: 1px dashed #1DB954;">Spotify Integration</span>  
7. <span style="border-bottom: 1px dashed #1DB954;">Triển khai</span>  
8. <span style="border-bottom: 1px dashed #1DB954;">Đóng góp</span>  -->

</div>


# Tổng quan

<div style="background-color: #1a1a1a; padding: 20px; border: 1px solid #333; border-radius: 5px; color: #fff; font-family: Arial, sans-serif;">
  
  <h3 style="color: #ccc; margin-bottom: 10px;">Backend xây dựng:</h3>
  <ul style="list-style-type: none; padding-left: 0; color: #fff;">
    <li style="margin-bottom: 5px;">Xác thực OAuth2 với Spotify</li>
    <li style="margin-bottom: 5px;">Lưu trữ token (MySQL)</li>
    <li style="margin-bottom: 5px;">Cung cấp API cho Frontend ReactJS</li>
<!--     <li style="margin-bottom: 5px; color: #888;">• Tự động làm mới token</li> -->
  </ul>
</div>

# Công nghệ

<div style="background-color: #1a1a1a; padding: 20px; border: 1px solid #333; border-radius: 5px; color: #fff; font-family: Arial, sans-serif;">
  <ul style="list-style-type: none; padding-left: 0; color: #fff;">
    <li style="margin-bottom: 5px;">Framework: Django 4.2 + Django REST Framework</li>
    <li style="margin-bottom: 5px;">Database: MySQL 8.0</li>
    <li style="margin-bottom: 5px;">Authentication: JWT + Spotify OAuth2</li>
<!--     <li style="margin-bottom: 5px;">• API Docs: Swagger/Redoc</li> -->
  </ul>
</div>

# Yêu cầu hệ thống

<div style="background-color: #1a1a1a; padding: 20px; border: 1px solid #333; border-radius: 5px; color: #fff; font-family: Arial, sans-serif; margin-top: 20px;">
  <ul style="list-style-type: none; padding-left: 0; color: #fff;">
    <li style="margin-bottom: 5px;">Python 3.10+</li>
    <li style="margin-bottom: 5px;">MySQL 8.0+</li>
<!--     <li style="margin-bottom: 5px;">Redis (cho Celery - optional)</li> -->
  </ul>
</div>

<h2>Cài đặt</h2>
  <p><strong>Cài đặt gói phụ thuộc:</strong></p>
  <pre style="background-color: #000; padding: 10px; border-radius: 4px;">pip install -r requirements.txt</pre>

  <p>Hoặc cài từng gói riêng lẻ:</p>
  <pre style="background-color: #000; padding: 10px; border-radius: 4px;">
sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config
pip install djangorestframework-simplejwt
pip install PyJWT
pip install mysqlclient
pip install django-cloudinary-storage cloudinary

  </pre>
</div>

<!-- Biến môi trường -->
<h2>Biến môi trường</h2>
<div style="background-color: #1a1a1a; padding: 20px; border: 1px solid #333; border-radius: 5px; color: #fff; font-family: Arial, sans-serif;">
  <p>Tạo file <code>.env.local</code> và thêm các biến sau:</p>
  <pre style="background-color: #000; padding: 10px; border-radius: 4px;">
CLERK_PUBLISHABLE_KEY="pk_test_..."
CLERK_JWKS_URL="https://your-app.clerk.accounts.dev/.well-known/jwks.json"
ADMIN_EMAIL="youremailhere@gmail.com"
  </pre>

  <p><strong>Cách lấy thông tin Clerk:</strong></p>
  <ul style="list-style-type: none; padding-left: 0;">
    <li>Đăng ký tại <a href="https://clerk.dev" style="color: #4da6ff;">clerk.dev</a></li>
    <li>Tạo ứng dụng mới → API Keys để lấy <code>Publishable Key</code></li>
    <li>Bật <code>ID Token</code> trong phần JWT Templates</li>
    <li>Copy link JWKS có đuôi như sau: <code>/.well-known/jwks.json</code></li>
  </ul>
</div>

 
<h2>Cấu hình Database</h2>

<h2> Các bước setup và seed dữ liệu cho project</h2>

<h3>Bước 1: Tạo database trong MySQL</h3>
<pre><code>CREATE DATABASE spotify_clone;
</code></pre>
<p>-> Mở MySQL terminal hoặc dùng công cụ như phpMyAdmin/MySQL Workbench để thực hiện lệnh này.</p>

<hr />

<h3>Bước 2: Cấu hình kết nối database trong Django</h3>
<p>Trong file <code>settings.py</code>, cập nhật cấu hình như sau:</p>
<pre><code>DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spotify_clone',
        'USER': 'tên_user',
        'PASSWORD': 'mật_khẩu',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
</code></pre>

<hr />

<h3>Bước 3: Chạy migrate để tạo bảng trong database</h3>
<pre><code>python manage.py makemigrations
python manage.py migrate
</code></pre>
<p> Lệnh này sẽ tạo các bảng trong database đã cấu hình ở bước trên.</p>

<hr />

<h3>Bước 4: Seed dữ liệu vào database</h3>
<p>File <code>seeddata.py</code> đã được viết sẵn trong thư mục <code>your_app/management/commands/</code>.</p>
<pre><code>python manage.py seeddata
</code></pre>
<p> Lệnh trên sẽ thêm các bài hát và album mẫu vào database.</p>

<hr />

<h3>Bước 5: Kiểm tra dữ liệu trong MySQL</h3>
<pre><code>USE spotify_clone;
SELECT * FROM spotify_app_song;
SELECT * FROM spotify_app_album;
</code></pre>
<p>Nếu bạn thấy dữ liệu trong bảng <code>song</code> và <code>album</code> thì bạn đã seed thành công!</p>
