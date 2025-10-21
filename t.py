from config import get_logger, settings

audit_log = get_logger("audit")
error_log = get_logger("error")

audit_log.info("User X updated record Y")
error_log.error("Failed to process request for user Z")

print(settings.internal_db_url)
print(settings.external_db_url)
print(settings.database_url)
