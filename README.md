# Mono Repo Microservices — CI Practice

## Cấu trúc
```
mono-microservices/
├── services/
│   ├── user-service/
│   ├── product-service/
│   ├── order-service/
│   └── notification-service/
├── .github/workflows/
│   └── ci.yml
├── requirements.txt        # dùng chung cho tất cả services
├── Makefile
└── README.md
```

## Services

| Service              | Port  | Mô tả                          |
|----------------------|-------|--------------------------------|
| user-service         | 8001  | Quản lý user (CRUD in-memory)  |
| product-service      | 8002  | Quản lý sản phẩm               |
| order-service        | 8003  | Tạo và xem đơn hàng            |
| notification-service | 8004  | Gửi thông báo (mock)           |

## Chạy nhanh
```bash
pip install -r requirements.txt
uvicorn services.user-service.app.main:app --reload --port 8001
```

## CI
GitHub Actions sẽ tự động chạy `pytest` cho từng service khi có push/PR.
