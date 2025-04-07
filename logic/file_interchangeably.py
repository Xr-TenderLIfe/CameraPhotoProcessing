# import os
# import shutil
#
# class FolderFilter:
#     def __init__(self, folder_a, folder_b, folder_c, selected_extensions_a, selected_extensions_b):
#         """
#         :param folder_a: 作为筛选条件的文件夹 A
#         :param folder_b: 需要筛选的文件夹 B
#         :param folder_c: 存放筛选后文件的文件夹 C
#         :param selected_extensions_a: A 文件夹中需要筛选的文件后缀（如 .txt, .csv）
#         :param selected_extensions_b: B 文件夹中可被复制的文件后缀（如 .wav, .mp3）
#         """
#         self.folder_a = folder_a
#         self.folder_b = folder_b
#         self.folder_c = folder_c
#         self.selected_extensions_a = {ext.lower() for ext in selected_extensions_a}
#         self.selected_extensions_b = {ext.lower() for ext in selected_extensions_b}
#
#         # 确保目标文件夹 C 存在
#         os.makedirs(self.folder_c, exist_ok=True)
#
#     def get_filtered_filenames(self):
#         """ 获取 A 文件夹中符合指定后缀的文件名（不包含后缀） """
#         return {
#             os.path.splitext(file)[0]  # 只取文件名
#             for file in os.listdir(self.folder_a)
#             if os.path.splitext(file)[1].lower() in self.selected_extensions_a
#         }
#
#     def filter_and_copy(self,update_progress_callback=None):
#         """ 在 B 文件夹中筛选符合 A 文件名，并且后缀符合 selected_extensions_b 的文件，复制到 C """
#         selected_files = self.get_filtered_filenames()
#         total_files = len(os.listdir(self.folder_b))
#         copied_count = 0
#
#         print(f"🔍 A 目录匹配的文件名数量：{len(selected_files)}")
#
#         for idx, file in enumerate(os.listdir(self.folder_b), 1):
#             file_base, file_ext = os.path.splitext(file)
#             file_ext = file_ext.lower()  # 统一小写处理
#
#             if file_base in selected_files and file_ext in self.selected_extensions_b:
#                 src_path = os.path.join(self.folder_b, file)
#                 dst_path = os.path.join(self.folder_c, file)
#
#                 if os.path.isfile(src_path):
#                     try:
#                         shutil.copy2(src_path, dst_path)
#                         copied_count += 1
#                         print(f"✅ [{idx}/{total_files}] 复制 {file} 到 {self.folder_c}")
#
#                         # 更新进度条（如果回调函数存在）
#                         if update_progress_callback:
#                             progress = int((idx / total_files) * 100)  # 计算进度
#                             update_progress_callback(progress)
#                     except Exception as e:
#                         print(f"❌ 复制失败: {file} - {e}")
#
#         print(f"\n🎯 文件筛选和复制完成！共复制 {copied_count} 个文件。")
#         # yield copied_count
#
# # 示例用法
# if __name__ == "__main__":
#     folder_a = r"A文件夹路径"
#     folder_b = r"B文件夹路径"
#     folder_c = r"C文件夹路径"
#
#     selected_extensions_a = [".txt", ".csv"]  # A 目录筛选的文件后缀
#     selected_extensions_b = [".wav", ".mp3", ".flac"]  # B 目录中符合后缀的文件才会被复制
#
#     filter_obj = FolderFilter(folder_a, folder_b, folder_c, selected_extensions_a, selected_extensions_b)
#     filter_obj.filter_and_copy()
from PyQt5.QtCore import QThread, pyqtSignal
import os
import shutil

class FolderFilter(QThread):
    progress_updated = pyqtSignal(int)  # 进度信号，传递整数（0-100）
    task_finished = pyqtSignal()  # 任务完成信号

    def __init__(self, folder_a, folder_b, folder_c, selected_extensions_a, selected_extensions_b):
        super().__init__()
        self.folder_a = folder_a
        self.folder_b = folder_b
        self.folder_c = folder_c
        self.selected_extensions_a = selected_extensions_a
        self.selected_extensions_b = selected_extensions_b
        self.is_running = True  # 控制线程是否继续执行

    def get_filtered_filenames(self):
        """ 模拟获取 A 目录中符合条件的文件名 """
        return set(os.path.splitext(f)[0] for f in os.listdir(self.folder_a))

    def run(self):
        """ 运行筛选和复制文件的任务 """
        selected_files = self.get_filtered_filenames()
        total_files = len(os.listdir(self.folder_b))
        copied_count = 0

        print(f"🔍 A 目录匹配的文件名数量：{len(selected_files)}")

        for idx, file in enumerate(os.listdir(self.folder_b), 1):
            if not self.is_running:  # 如果线程被要求停止，则退出
                break

            file_base, file_ext = os.path.splitext(file)
            file_ext = file_ext.lower()  # 统一小写处理

            if file_base in selected_files and file_ext in self.selected_extensions_b:
                src_path = os.path.join(self.folder_b, file)
                dst_path = os.path.join(self.folder_c, file)

                if os.path.isfile(src_path):
                    try:
                        shutil.copy2(src_path, dst_path)
                        copied_count += 1
                        print(f"✅ [{idx}/{total_files}] 复制 {file} 到 {self.folder_c}")

                        # 计算进度并发送信号
                        progress = int((idx / total_files) * 100)
                        self.progress_updated.emit(progress)

                    except Exception as e:
                        print(f"❌ 复制失败: {file} - {e}")

        print(f"\n🎯 文件筛选和复制完成！共复制 {copied_count} 个文件。")
        self.task_finished.emit()  # 任务完成后，发送信号

    def stop(self):
        """ 停止任务 """
        self.is_running = False
