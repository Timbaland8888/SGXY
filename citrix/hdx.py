from time import sleep

import win32api
import win32con
import win32gui


def get_child_windows(parent):
    '''
    获得parent的所有子窗口句柄
     返回子窗口句柄列表
     '''
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd),  hwndChildList)
    return hwndChildList
if __name__ == '__main__':
    flag = 0
    while True:

        try:
            hwnd = win32gui.FindWindow('#32770', 'HDX 文件访问')
            # left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            # print(left,top,right,bottom)

            result = get_child_windows(hwnd)
            # print(result)
            for  i  in result:
                title = win32gui.GetWindowText(i)
                clsname = win32gui.GetClassName(i)
                if title == '读取/写入权限(&W)' and clsname=='Button':
                    left, top, right, bottom = win32gui.GetWindowRect(i)
                    win32api.SetCursorPos([left, top])
                    print(f'读取、写入句柄：{i}')
                    print(left, top, right, bottom)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, left, top, right, bottom)
                    flag = 1
                    # win32api.keybd_event(left, top, win32con.KEYEVENTF_KEYUP, bottom)

        except Exception as e:
            print('HDX 文件访问未启用')
            pass
        sleep(0.5)
        if flag == 1:
            break
