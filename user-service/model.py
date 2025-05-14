from sqlalchemy import Column, String, Boolean, DateTime, Float, UUID
from sqlalchemy.sql import func
import uuid
from config.database import Base

# Don't have multiple UUID's keep it simple and stick with one which will be used across the entire application and all the services.
# | Field          | Type       | Required | Notes                                                      |
# | -------------- | ---------- | -------- | ---------------------------------------------------------- |
# | `id`           | UUID / int | ✅        | Internal unique user ID                                    |
# | -------------- | ---------- | -------- | ---------------------------------------------------------- |

# User Service database schema for MVP trading platform
# | Field          | Type       | Required | Notes                                                       |
# | -------------- | ---------- | -------- | ----------------------------------------------------------  |
# | `firebase_uid` | string     | ✅        | Link to Firebase Auth                                      |
# | `email`        | string     | ✅        | Used for notifications & Firebase login                    |
# | `full_name`    | string     | ✅        | Name for display                                           |
# | `created_at`   | datetime   | ✅        | Signup timestamp                                           |
# | `updated_at`   | datetime   | ✅        | Signup timestamp                                           |
# | `last_logged_in`   | datetime   | ✅        | Signup timestamp                                       |
# | `role`         | string     | ✅        | `user`, `admin`, `trader` etc. (default: `user`)           |
# | `is_active`    | boolean    | ✅        | Account status                                             |
# | `balance`      | float      | optional | For demo account trading (if applicable)                    |
# | `kyc_status`   | string     | optional | `pending`, `approved`, `rejected` (if you plan to add KYC)  |
# | `country`      | string     | optional | Can be useful for legal/compliance reasons                  |
# | `phone number` | string     | optional | Can be useful for legal/compliance reasons                  |
# | `preferred_currency` | string     | optional | Can be useful for legal/compliance reasons            |
# | -------------- | ---------- | -------- | ----------------------------------------------------------  |

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    # firebase_uid = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_logged_in_at = Column(DateTime(timezone=True), nullable=True)
    role = Column(String, default="user", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    balance = Column(Float, nullable=True)
    kyc_status = Column(String, nullable=True)
    country = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    preferred_currency = Column(String, nullable=True)
