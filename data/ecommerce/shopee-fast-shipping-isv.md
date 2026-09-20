---
doc_id: shopee-fast-shipping-isv
title: Hướng dẫn xử lý đơn Gói Sẵn Giao Nhanh (ISV)
audience: seller
category: order-processing
language: vi
source_url: https://banhang.shopee.vn/edu/article/20537
retrieved_at: 2026-09-20
document_version: "2024-09-20"
---

# Hướng dẫn xử lý đơn hàng trong chương trình Gói Sẵn Giao Nhanh - Dành cho Người Bán sử dụng ISV

## A. Đối tượng áp dụng

### 1. Chương trình Gói sẵn giao nhanh Shopee là gì?
Ra mắt từ tháng 08/2024, chương trình Gói sẵn giao nhanh là một sáng kiến đột phá nhằm rút ngắn thời gian chờ đợi của Người Mua khi mua sắm trên Shopee. 
Đơn hàng trong chương trình này sẽ được giao đến Người Mua trong thời gian nhanh nhất có thể, đặc biệt là Người Mua ở ngoại tỉnh.

### 2. ISV là gì?
ISV (Enterprise 3rd party) là phần mềm bên thứ 3 giúp quản lý đơn hàng như Nhanhvn, Sapo, Salework v.v.

### 3. Người Bán Shopee sử dụng ISV là gì?
Người Bán Shopee sử dụng ISV (đã gọi API với Kênh Người Bán Shopee) để tiến hành xác nhận đơn hàng Shopee, theo dõi hoặc quản lý đơn hàng thông qua ISV.

## B. Hướng dẫn xử lý đơn hàng dành cho Người Bán Shopee sử dụng ISV

### 1. Đối với Người Bán đang sử dụng dịch vụ của ISV BigSeller

#### a) Kiểm tra đơn hàng
Để xem đây có phải là đơn hàng thuộc chương trình "Gói sẵn giao nhanh" hay không, Người Bán cần thực hiện các bước sau:
- Bước 1: Truy cập trang BigSeller
- Bước 2: Vào Đơn hàng mục Xử lý đơn hàng và chọn Chờ xử lý
- Bước 3: Ở bộ lọc, chọn Sàn TMĐT Shopee và loại hình đơn hàng: Đơn Gói Sẵn Giao Nhanh để xem danh sách đơn hàng cần xử lý.

#### b) Xử lý đơn hàng và giao cho đơn vị vận chuyển (ĐVVC)
Người Bán xử lý đơn hàng thuộc chương trình Đơn Gói Sẵn Giao Nhanh và giao cho ĐVVC tương tự quy trình xử lý những đơn hàng bình thường được đặt bởi Người Mua.
Sau khi Người Bán giao hàng thành công cho ĐVVC, đơn hàng sẽ được ghi nhận tại mục Đơn hàng > Xử lý đơn hàng > Nền tảng đang xử lý > Sàn TMĐT Shopee > Loại hình đơn hàng: Đơn Gói Sẵn Giao Nhanh.

#### c) Theo dõi đơn hàng hoàn trả
Để xem các đơn hàng không được gán thành công, Người Bán cần truy cập mục Đơn hàng > Xử lý đơn hàng > Hủy đơn hàng > Đã hủy > Sàn TMĐT Shopee > Loại hình đơn hàng: Đơn Gói Sẵn Giao Nhanh > Trạng thái trước khi hủy: Nền tảng đang xử lý.
Trường hợp đơn hàng sau 7 ngày lưu kho được hoàn trả cho Người Bán do gán đơn thực tế không thành công, Người Bán sẽ được miễn chi phí vận chuyển 2 chiều đối với các đơn này.

### 2. Đối với Người Bán đang sử dụng dịch vụ của ISV Salework

#### a) Kiểm tra đơn hàng
- Bước 1: Truy cập trang Salework
- Bước 2: Chọn Kênh Shopee GSGN
- Bước 3: Vào Xử lý đơn hàng mục Chuẩn bị hàng để xem danh sách đơn hàng Gói Sẵn Giao Nhanh cần xử lý.

#### b) Xử lý đơn hàng và giao cho đơn vị vận chuyển (ĐVVC)
Sau khi Người Bán giao hàng thành công cho ĐVVC, đơn hàng sẽ được ghi nhận tại mục Kênh Shopee GSGN > Danh sách đơn hàng > Đã gửi hàng. Sau đó, đơn hàng đang được vận chuyển sẽ chuyển qua mục Đang giao.

#### c) Theo dõi đơn hàng hoàn trả
Để xem các đơn hàng không được gán thành công, Người Bán cần truy cập mục Hoàn tại Kênh Shopee GSGN > Danh sách đơn hàng.
Trường hợp đơn hàng sau 7 ngày lưu kho được hoàn trả cho Người Bán, Người Bán sẽ được miễn chi phí vận chuyển 2 chiều.

> **⚠️ Lưu ý chung:** Nếu Người Bán chưa nhận được hàng/đơn hàng hoàn trả về không nguyên vẹn, Người Bán có thể gửi khiếu nại để được Shopee xem xét và giải quyết.

## C. Các câu hỏi thường gặp

**1. Nếu có câu hỏi về cách thức xử lý hoặc quản lý đơn Gói Sẵn Giao Nhanh trên ISV thì Người Bán có thể liên hệ với ai?**
Người Bán vui lòng liên hệ trực tiếp với phía ISV để được hỗ trợ.
