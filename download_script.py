from downloader import Downloader

if __name__ == "__main__":
    print("Configuring")
    downloader = Downloader(True)
    downloader.configure()
    downloader.make_client()
    print("Fetching data")
    downloader.fetch()
    print("Saving to csv files")
    downloader.to_csv('data')
