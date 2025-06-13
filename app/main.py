from sync.sync_service import DataSyncService

def main():
    sync_service = DataSyncService("users")
    sync_service.sync()

if __name__ == "__main__":
    main()