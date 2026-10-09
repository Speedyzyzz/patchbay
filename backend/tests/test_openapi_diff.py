from app.diff.openapi_diff import OpenAPIDiffDetector
from app.diff.change_taxonomy import ChangeCategory

def test_detect_endpoint_rename():
    old_spec = {
        "paths": {
            "/api/v1/users": {
                "summary": "Fetch users list"
            }
        }
    }
    new_spec = {
        "paths": {
            "/api/v2/accounts": {
                "summary": "Fetch users list"  # Summary matched
            }
        }
    }

    changes = OpenAPIDiffDetector.compare_specs(old_spec, new_spec)
    assert len(changes) == 1
    assert changes[0].category == ChangeCategory.ENDPOINT_RENAME
    assert changes[0].replacement_symbol == "/api/v2/accounts"

def test_detect_param_addition():
    old_spec = {
        "paths": {
            "/api/items": {
                "get": {
                    "parameters": [{"name": "id", "required": True}]
                }
            }
        }
    }
    new_spec = {
        "paths": {
            "/api/items": {
                "get": {
                    "parameters": [
                        {"name": "id", "required": True},
                        {"name": "org_id", "required": True, "type": "string"}
                    ]
                }
            }
        }
    }

    changes = OpenAPIDiffDetector.compare_specs(old_spec, new_spec)
    assert len(changes) == 1
    assert changes[0].category == ChangeCategory.PARAM_ADDED
    assert changes[0].new_signature["param"] == "org_id"
