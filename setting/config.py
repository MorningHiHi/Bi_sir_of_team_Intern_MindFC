import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Core PostgreSQL Example")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "False").lower() == "true"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "sangnguyenthac")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "123456")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "test_db")

    """@property là để hàm này tính toán các dữ liệu dựa trên các thuộc tính đã gán ở trên  sau đó lưu dữ liệu đó vào tên của hàm đó để lưu trữ như một biến """

    @property 
    def DATABASE_URL(self): 
        #self đại diện cho chính đối tượng hiện tại nó trỏ đến chính nó, tương đương như đối tượng "this" trong java hay c#
        if self.POSTGRES_PASSWORD:
            return (
                f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        else:
            return (
                f"postgresql+psycopg2://{self.POSTGRES_USER}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )

settings = Settings() 
"""khi biên dịch thì dòng lệnh trên được chạy vì Settings() là một lời gọi khởi tạo đối tượng và vì các thuốc tính được cấu hình mặc định tự dộng thực thi nên dù hàm không viết __init__ thì thì __init__ mặc định sẽ tự khởi tạo đối tượng (default contructor) tạo các thông tin cần thiết--> như biết khi from setting.config import settings được chỉ định trong các file thì nó tự động thực thi theo logic trên và trả về dữ liệu thông qua biến settings để sử dụng"""
