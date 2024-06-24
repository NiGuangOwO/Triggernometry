import os
import ctypes
import sys
import re
import requests
from typing import Optional, List
import webbrowser

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    print("一键安装触发器/鲶鱼精邮差 by 阿洛\n————————————————————")
    if not is_admin():
        input("请使用管理员权限打开程序。")
        return
    while True:
        try:
            act_type = input("\n请选择你使用的 ACT 版本：\n1. 原版\n2. 呆萌整合\n3. CafeACT\n").strip()
            match act_type:
                case "1":
                    home = os.getenv('APPDATA')
                    config_path = os.path.join(home, "Roaming", "Advanced Combat Tracker", "Config", "Advanced Combat Tracker.config.xml")
                    plugin_path = os.path.join(home, "Roaming", "Advanced Combat Tracker", "Plugins")
                    print("请确保：\n")
                    print("1. 该程序已置于 ACT 根目录下；")
                    print("2. 当前没有正在运行的 ACT。")
                    print("3. 你需要确保已经安装了 FF14 解析插件、ngld/OverlayPlugin 悬浮窗，并重启过 ACT。")
                    input("\n确认以上内容后回车继续。")
                case "2":
                    current_location = os.getcwd()
                    config_path = os.path.join(current_location, "Config", "Advanced Combat Tracker.config.xml")
                    plugin_path = os.path.join(current_location, "Plugins")
                    print("请确保：\n")
                    print("1. 该程序已置于 ACT 根目录下；")
                    print("2. 当前没有正在运行的 ACT。")
                    input("\n确认以上内容后回车继续。")
                case "3":
                    current_location = os.getcwd()
                    config_path = os.path.join(current_location, "AppData", "Advanced Combat Tracker", "Config", "CafeACT.config.xml")
                    plugin_path = os.path.join(current_location, "Plugins")
                    print("请确保：\n")
                    print("1. 该程序已置于 ACT 根目录下；")
                    print("2. 当前没有正在运行的 ACT。")
                    print("3. 你需要确保在插件中心安装了 FF14 解析插件、ngld/OverlayPlugin 悬浮窗、Triggernometry，并重启过 ACT。")
                    input("\n确认以上内容后回车继续。")
                case _:
                    print("输入必须是 1 / 2 / 3。请重新输入。")
                    continue
            if act_type == "3":
                is_CN = True
            else:                
                match input("\n请选择 ACT 对应的客户端：\n1. 国服\n2. 国际服\n").strip():
                    case "1":
                        is_CN = True
                    case "2":
                        is_CN = False
                    case _:
                        print("输入必须是 1 / 2。请重新输入。")
                        continue
            set_up_config(config_path, plugin_path, is_CN)
            input("你可以直接退出程序，或按回车键打开资源网盘，内含分享的触发器资源。")
            webbrowser.open("https://www.123pan.com/s/1xRXjv-340BH.html", new=2)
            break
        except Exception as e:
            input(f"发生错误: {e}")

class Plugin:

    def __init__(self, enabled: bool | str, full_path: str) -> None:
        if isinstance(enabled, str):
            self.enabled = 'True' if enabled.strip().lower() == 'true' else 'False'
        else:
            self.enabled = 'True' if enabled else 'False'
        self.full_path = full_path
        self.folder_path, self.name = self.full_path.rsplit('\\', 1)

    @staticmethod
    def parse(rawXml: str) -> 'Plugin':
        enabled_match = re.search(r'Enabled="(.*?)"', rawXml)
        enabled = enabled_match.group(1) if enabled_match else 'False'

        path_match = re.search(r'Path="(.*?)"', rawXml)
        full_path = path_match.group(1) if path_match else ''

        return Plugin(enabled, full_path)

    def to_xml_string(self) -> str:
        return f"\n        <Plugin Enabled=\"{self.enabled}\" Path=\"{self.full_path}\" />"
    
    # 从远程地址更新并覆盖本地插件。若提供 file_name，则更新并覆盖本地插件同文件夹下的指定名称文件（如触发器汉化）。
    def update(self, remote_path: str, file_name: Optional[str] = None) -> None:
        path = self.full_path if file_name is None else os.path.join(self.folder_path, file_name)
        file_name = self.name if file_name is None else file_name
        print(f"\n正在从 {remote_path} 下载 {file_name} ...")
        try:
            response = requests.get(remote_path)
            response.raise_for_status()
            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"已成功安装或更新：{file_name}")
        except requests.RequestException as e:
            print(f"从 {remote_path} 下载 {file_name} 失败: \n{e}\n")
        except IOError as e:
            print(f"数据写入 {file_name} 失败：\n{e}\n")
    
    def delete(self) -> None:
        try:
            os.remove(self.full_path)
        except:
            pass

def get_plugin_from_list(plugin_name: str, plugin_list: List[Plugin]) -> Optional[Plugin]:
    for plugin in plugin_list:
        if plugin_name.lower() in plugin.name.lower():
            return plugin
    return None

REMOTE_FOLDER = "https://vip.123pan.cn/1824544011/Triggernometry_Release_CN/"

def set_up_config(config_path: str, plugin_path: str, is_CN: bool):

    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            xml_data = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("错误：配置文件不存在。你可能选择了错误的 ACT 版本，或程序未置于根目录。")

    matches = list(re.finditer(r'<ActPlugins>(.*?)</ActPlugins>', xml_data, re.DOTALL))

    if not matches:
        print("配置文件中未找到 <ActPlugins>。")
    else:
        match = matches[-1] # 呆萌整合版开头有另外一处 <ActPlugins>
        act_plugins_content = match.group(1)
        raw_plugins = re.findall(r'<Plugin .*?/>', act_plugins_content)
        act_plugins = [Plugin.parse(plugin_xml) for plugin_xml in raw_plugins]

        # Triggernometry
        mlm_trig = get_plugin_from_list("MlmTr", act_plugins)
        if mlm_trig is None:
            mlm_trig = get_plugin_from_list("莫灵喵", act_plugins)
        if mlm_trig is not None:
            mlm_trig.delete()
            act_plugins.remove(mlm_trig)

        trig = get_plugin_from_list("Triggernometry", act_plugins)
        if trig is None:
            trig = Plugin('True', os.path.join(plugin_path, "Triggernometry.dll"))
        
            if parser := get_plugin_from_list("FFXIV_ACT_Plugin", act_plugins):
                index = act_plugins.index(parser) + 1
            else:
                index = (length := len(act_plugins)) if length <= 2 else 2
            act_plugins.insert(index, trig)

        trig.update(REMOTE_FOLDER + "Triggernometry.dll")
        trig.update(REMOTE_FOLDER + "zh-CN.triglations.xml", "zh-CN.triglations.xml")

        # PostNamazu
        namazu = get_plugin_from_list("PostNamazu", act_plugins)
        if namazu is None:
            namazu = Plugin('True', os.path.join(plugin_path, "PostNamazu.dll"))
            act_plugins.append(namazu)
        if is_CN:
            namazu.update(REMOTE_FOLDER + "PostNamazuCN.dll")
        else:
            namazu.update(REMOTE_FOLDER + "PostNamazuInt.dll")

        modified_content = ''.join([p.to_xml_string() for p in act_plugins]) + "\n    "
        new_xml_data = xml_data.replace(act_plugins_content, modified_content)

        with open(config_path, 'w', encoding='utf-8') as file:
            file.write(new_xml_data)
        with open(config_path + '_', 'w', encoding='utf-8') as file:
            file.write(new_xml_data)
        print("已完成初始化。")

if __name__ == "__main__":
    main()
