## packageUploadApp

- Android自动打包并上传到fir.im
- 渠道包
- 签名并添加渠道包

## Usage
1. 在`package.config`文件中配置fir.im的api_token

2. 因为在项目中使用了[requests](https://github.com/requests/requests)来发请求，所以需要你安装该包
`brew install pipenv`
`pipenv install requests`

3. python3 xxx/packageAndroid.py
