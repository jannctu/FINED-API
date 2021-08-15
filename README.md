# Serve FINED Model as API

This repository contains the service for our FINED Model, details of our paper:

**[FINED: Fast Inference Network for Edge Detection](https://www.computer.org/csdl/proceedings-article/icme/2021/09428230/1uimbqYAE9i)**

by Jan Kristanto Wibisono , Hsueh-Ming Hang   
[Official Repository](https://github.com/jannctu/FINED)
# Homepage 
Please visit our model deployment at [lab1.jankristanto.com](https://lab1.jankristanto.com)

# API
Swagger UI doc : [lab1.jankristanto.com/docs](https://lab1.jankristanto.com/docs)

### Example:

```python 
import requests
def test_image(url,image_url):
    response = requests.request("GET", url+"?img_url="+image_url)
    with open("edge2.png", 'wb') as f:
        f.write(response.content)

if __name__ == "__main__":
    url = 'https://lab1.jankristanto.com/predict/url'
    image_url = 'https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png'
    test_image(url,image_url)
```
![image](https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png)
![image](https://lab1.jankristanto.com/static/img/edge2.png)

# Citing
Thanks for your interest in our work, please consider citing:

    ```
    @INPROCEEDINGS{
	    9428230,
		author={Wibisono, Jan Kristanto and Hang, Hsueh-Ming},
		booktitle={2021 IEEE International Conference on Multimedia and Expo (ICME)}, 
		title={Fined: Fast Inference Network for Edge Detection}, 
		year={2021},
		volume={},
		number={},
		pages={1-6},
		doi={10.1109/ICME51207.2021.9428230}
	}
	```