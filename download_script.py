from downloader import Downloader

if __name__ == "__main__":
    print("Configuring")
    downloader = Downloader(True)
    downloader.configure()
    downloader.make_client()
    downloader.fetch()
    downloader.to_csv('data')
