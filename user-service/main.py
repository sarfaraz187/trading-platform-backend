# User Service database schema for MVP trading platform
# | Field          | Type       | Required | Notes                                                      |
# | -------------- | ---------- | -------- | ---------------------------------------------------------- |
# | `id`           | UUID / int | ✅        | Internal unique user ID                                    |
# | `firebase_uid` | string     | ✅        | Link to Firebase Auth                                      |
# | `email`        | string     | ✅        | Used for notifications & Firebase login                    |
# | `full_name`    | string     | ✅        | Name for display                                           |
# | `created_at`   | datetime   | ✅        | Signup timestamp                                           |
# | `role`         | string     | ✅        | `user`, `admin`, `trader` etc. (default: `user`)           |
# | `is_active`    | boolean    | ✅        | Account status                                             |
# | `balance`      | float      | optional | For demo account trading (if applicable)                   |
# | `kyc_status`   | string     | optional | `pending`, `approved`, `rejected` (if you plan to add KYC) |
# | `country`      | string     | optional | Can be useful for legal/compliance reasons                 |
# | `phone number` | string     | optional | Can be useful for legal/compliance reasons                 |
# | `preferred_currency` | string     | optional | Can be useful for legal/compliance reasons                 |

