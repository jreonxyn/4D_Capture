import os
import sys
import time
import cv2
import requests
import subprocess
import signal
import shlex
from requests_toolbelt import *


def use_guide():
    print("         欢迎使用            ")
    print(f"1 -> starting rec\n"
          f"2 -> save and delete all files\n"
          f"3 -> stopping rec\n"
          f"4 -> delete file by url\n"
          f"5 -> show all files\n"
          f"6 -> save file bu url\n"
          f"7 -> save all files\n"
          f"8 -> delete all files\n")


class ZCAMController:

    def __init__(self):
        self.master_ip = "192.168.1.6"

        self.all_ips = [
            "192.168.1.6",
            "192.168.1.8",
            "192.168.1.9"
        ]

        # self.master_ip = "192.168.0.102"
        #
        # self.all_ips = [
        #     "192.168.0.102",
        #     "192.168.0.100",
        #     # "192.168.1.9"
        # ]

    def start_rec(self):
        url = f"http://{self.master_ip}/ctrl/rec?action=start"
        res = requests.get(url).json()

        if res["code"] == 0:
            print("[controller Info] ==> Start REC")
        else:
            print("Error when start REC")

    def stop_rec(self):
        url = f"http://{self.master_ip}/ctrl/rec?action=stop"
        res = requests.get(url).json()

        if res["code"] == 0:
            print("[controller Info] ==> Stop REC")
        else:
            print("Error when stop REC")

    def save_and_delete_all_files(self, save_all=False, delete_all=False):
        all_files = self.get_all_files()
        for file in all_files:
            path_info = file.split("/")
            save_path = path_info[2] + "/" + path_info[4]
            video = path_info[5]
            if save_all:
                self.download_video(file, save_path, video)
            if delete_all:
                self.delete_video(file)

    def get_all_files(self):
        all_files = []
        for ip in self.all_ips:
            url1 = f"http://{ip}/DCIM/"
            res1 = requests.get(url1).json()
            files = res1["files"]
            for file in files:
                url2 = url1 + f"{file}"
                res2 = requests.get(url2).json()
                videos = res2["files"]
                for video in videos:
                    url_video = url2 + f"/{video}"

                    all_files.append(url_video)

        return all_files

    def show_all_files(self):
        print("[controller Info] ==> all files are below")
        all_files = self.get_all_files()
        for file in all_files:
            print(file)

        print(f"totally {len(all_files)} files")

    def save_video(self, url):
        path_info = url.split("/")
        save_path = path_info[2] + "/" + path_info[4]
        video = path_info[5]
        self.download_video(url, save_path, video)

    @staticmethod
    def download_video(url, save_path, video):
        os.makedirs(f"./files/{save_path}", exist_ok=True)
        video_name = f"./files/{save_path}/{video}"

        res = requests.get(url, stream=True)
        total_length = float(res.headers['content-length'])
        count = 0
        count_tmp = 0
        time_step = 2

        time0 = time.time()

        with open(video_name, "wb") as file:
            for chunk in res.iter_content(chunk_size=512):
                if chunk:
                    file.write(chunk)
                    count += len(chunk)

                    if time.time() - time0 > time_step:
                        progress = round(count / total_length * 100, 2)
                        speed = round((count - count_tmp) / 1024 / 1024 / time_step, 2)
                        count_tmp = count
                        time0 = time.time()

                        print(f"downloading from {url}, progress: {progress}%, speed: {speed}M/s")

        print(f"[controller Info] ==> Downloaded - {url}")


    @staticmethod
    def delete_video(url):
        res = requests.get(url + "?act=rm").json()
        if res["code"] == 0:
            print(f"[controller Info] ==> Deleted - {url}")
        else:
            print(f"[controller Info] ==> Error - when deleting {url}")


class KinectController:

    def __init__(self):
        self.process = None
        self.save_path = "D:/projects/4D_Face_Capture/4D_Capture/controller/offline/files/kinect/K001"
        self.cwd = "C:/Program Files/Azure kinect SDK v1.4.1/tools/"
        self.shell_cmd = "k4arecorder.exe -c 2160p " + self.save_path + "/out_4.mkv"
        self.cmd = shlex.split(self.shell_cmd)

    def start_rec(self):
        self.process = subprocess.Popen(args=self.cmd, cwd=self.cwd, shell=True)

    def stop_rec(self):
        try:
            os.kill(0, signal.CTRL_C_EVENT)
        except KeyboardInterrupt:
            print("except")


if __name__ == '__main__':
    controller = ZCAMController()
    kinect_controller = KinectController()

    use_guide()

    is_rec = False

    while True:
        try:
            command = int(input("\n请输入指令进行操作: "))
        except KeyboardInterrupt:
            print(f"[command error] ==> 请重新输入指令进行操作")
            continue
        if command == 1:
            if is_rec:
                print(f"[command Info] ==> 正在录制中，请先结束录制")
            else:
                controller.start_rec()
                kinect_controller.start_rec()
                is_rec = True
        elif command == 2:
            print("[command Info] ==> 正在下载数据")
            controller.save_and_delete_all_files(save_all=True, delete_all=True)
            print("[command Info] ==> 下载完毕")
        elif command == 3:
            if is_rec:
                controller.stop_rec()
                kinect_controller.stop_rec()
                is_rec = False
            else:
                print("[command Info] ==> 请先开始录制")
        elif command == 4:
            url = input("请输入待删除的文件的 url: ")
            if url in controller.get_all_files():
                controller.delete_video(url)
                print("[command Info] ==> 删除成功 " + url)
            else:
                print("url 输入有误")
        elif command == 5:
            controller.show_all_files()
        elif command == 6:
            url = input("请输入待下载的文件的 url: ")
            if url in controller.get_all_files():
                controller.save_video(url)
                print("[command Info] ==> 下载成功 " + url)
            else:
                print("url 输入有误")
        elif command == 7:
            print("[command Info] ==> 正在下载所有数据")
            controller.save_and_delete_all_files(save_all=True, delete_all=False)
            print("[command Info] ==> 下载完毕")
        elif command == 8:
            print("[command Info] ==> 正在删除所有数据")
            controller.save_and_delete_all_files(save_all=False, delete_all=True)
            print("[command Info] ==> 删除完毕")
        elif command == -1:
            if is_rec:
                print("[command Info] ==> 请先结束录制再退出")
            else:
                break
        else:
            print("[command Info] ==> 指令有误， 请重新输入")
