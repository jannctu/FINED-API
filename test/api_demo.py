import requests

def test_image(url,image_file):
    files = {
        'file' : open(image_file, 'rb')
    }
    response = requests.request("POST", url, files=files)
    with open("edge.png", 'wb') as f:
        f.write(response.content)

def test_image2(url,image_url):
    response = requests.request("GET", url+"?img_url="+image_url)
    with open("edge2.png", 'wb') as f:
        f.write(response.content)

if __name__ == "__main__":
    url = 'https://lab1.jankristanto.com/predict/image'
    fname = 'pandas.jpg'
    test_image(url,fname)
    url2 = 'https://lab1.jankristanto.com/predict/url'
    image_url = 'https://images.pexels.com/photos/736230/pexels-photo-736230.jpeg'
    test_image2(url2,image_url)