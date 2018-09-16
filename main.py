from api import Azureface, Baiduface, FacePP

af = Azureface()
bf = Baiduface()
fp = FacePP()

# 单人照片
img_trump = "https://www.pcmarket.com.hk/wp-content/uploads/2018/03/usa-election_trump1-770x439_c.jpg"  # 特朗普怒竖指
# 多人照片
img_url_more1 = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1537109119958&di=184ceb74e77b081542163c6cea750822&imgtype=0&src=http%3A%2F%2Fn.sinaimg.cn%2Fsinacn11%2F709%2Fw400h309%2F20180319%2Ff469-fyskeuc0782277.jpg'
img_url_more2 = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1537121361422&di=ec91bd496cab92152c8c2786a50c02f0&imgtype=0&src=http%3A%2F%2Fimg2.tiandaoedu.com%2Fwww%2Fueditor%2Fnet%2Fupload%2F2016-01-19%2Fdb5942b5-7c25-4f54-9c9a-1d5508c566d0.jpg'


if __name__ == '__main__':
    af_info, bf_info, fp_info = [], [], []
    try:
        for img_url in [img_trump, img_url_more1, img_url_more2]:
            af_info.append(af.reconize_face(img_url=img_url))
            bf_info.append(bf.reconize_face(img_url=img_url))
            fp_info.append(fp.reconize_face(img_url=img_url))
    except Exception as e:
        print(e)

    print(af_info)
    print(bf_info)
    print(fp_info)


