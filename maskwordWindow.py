#!/usr/bin/python
# -*- coding: UTF-8 -*-

from baseWindow import *
import os
import sys
import lupa
import xlsxwriter

lua = lupa.LuaRuntime()
charList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
            "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN",
            "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ",
            "BA", "BB", "BC", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BK", "BL", "BM", "BN",
            "BO", "BP", "BQ", "BR", "BS", "BT", "BU", "BV", "BW", "BX", "BY", "BZ",
            "CA", "CB", "CC", "CD", "CE", "CF", "CG", "CH", "CI", "CJ", "CK", "CL", "CM", "CN",
            "CO", "CP", "CQ", "CR", "CS", "CT", "CU", "CV", "CW", "CX", "CY", "CZ"
            ]


def get_file_name(filename):
    (_, tmp) = os.path.split(filename)
    # print(_+"___"+tmp)
    # (f_name, ext) = os.path.splittext(tmp)
    return tmp


class SymbolicateWindow(BaseWindow):
    lua_tool = {}
    lua_libs = {}
    root_mapping = {}
    export_path = ""
    input_path = ""

    def __init__(self):
        super().__init__()
        self._init_lua_tool()

    def InitUI(self):
        usr_home = os.path.expanduser('~')
        # sys.path[0]
        full_path = usr_home + "\\PathConfig.lua"
        f = open(full_path, 'r')
        code_str = f.readlines()
        path_config = lua.execute('\n'.join(code_str))

        self.AddLabel('lua文件路径:')
        # self.inputCrashPath = self.AddInput(r'D:\test\lua\ActivityCondition.lua')
        # self.inputCrashPath = self.AddInput(r'D:\test\lua')
        # self.inputCrashPath = self.AddInput(path_config.luaPath)
        self.btnOpenLuaDir = self.AddBtn('设置lua文件夹', self.open_lua_dir, width=15)
        self.btnOpenLuaDir.place(x=300, y=1)
        self.btnOpenLuaFile = self.AddBtn('设置lua文件', self.open_lua_file, width=15)
        self.btnOpenLuaFile.place(x=450, y=1)
        self.inputCrashPath = self.AddInput(path_config.luaPath)
        # self.inputCrashPath.config(width=100)

        self.AddLabel('excel导出路径:')
        self.inputLibPath = self.AddInput(path_config.excelPath)
        self.btnOpenExcelDir = self.AddBtn('设置excel导出目录', self.open_excel_dir, width=15)
        self.btnOpenExcelDir.place(x=300, y=65)
        self.btnCrashPathSet = self.AddBtn('开始导出', self.lua2excel, width=15)
        self.btnCrashPathSet.place(x=450, y=65)
        self.AddLabel('输出状态:')
        self.outPutLog = self.AddLabel("等待操作")

    def DwWindow(self):
        self.SetScreenSize(650, 200)
        self.SetTitle('lua转excel')
        self.ShowWindow()

    def open_excel_dir(self):
        # self.inputLibPath.config(text=self.OpenDir())
        self.inputLibPath.delete(1.0, tkinter.END)
        self.inputLibPath.insert(1.0, self.OpenDir())

    def open_lua_dir(self):
        # self.inputCrashPath.config(text=self.OpenDir())
        self.inputCrashPath.delete(1.0, tkinter.END)
        self.inputCrashPath.insert(1.0, self.OpenDir())

    def open_lua_file(self):
        # self.inputCrashPath.config(text=self.OpenFile())
        self.inputCrashPath.delete(1.0, tkinter.END)
        self.inputCrashPath.insert(1.0, self.OpenFile())

    def _init_lua_tool(self):
        # print(sys.path[0]+"__"+sys.argv[0])
        usr_home = os.path.expanduser('~')
        full_path = usr_home + "\\LuaTool.lua"
        f = open(full_path, 'r')
        code_str = f.readlines()
        self.lua_tool = lua.execute('\n'.join(code_str))

    def lua2excel(self):
        self.outPutLog.config(text="开始导出")
        # print(self.inputLibPath.)
        self.export_path = self.inputLibPath.get(1.0, "end").replace('\n', '')
        self.input_path = self.inputCrashPath.get(1.0, "end").replace('\n', '')
        self.lua_libs = {}
        full_path = self.input_path
        if os.path.isfile(full_path):
            self.excute_lua_file(full_path)
        elif os.path.isdir(full_path):
            self.excute_lua_dir(full_path)
        self.outPutLog.config(text="导出完成")
        tkinter.messagebox.showinfo('提示', '导出完成')
        # self.content.OutputTxt(callstack,charArr,maskCharArr)

    def excute_lua_file(self, full_path):
        file_name = get_file_name(full_path)
        if ".lua" not in file_name:
            return
        # print(file_name)
        try:
            f = open(full_path, 'r', encoding='utf-8')
            code_str = f.readlines()
            # self.lua_libs[file_name] = lua.execute('\n'.join(code_str))
            # for luaTable in self.lua_libs.values():
            # lua_table = self.lua_tool.PrintLuaTable(luaTable, file_name)
            # self.print_lua_table(lua_table, file_name)
            luaTable = lua.execute('\n'.join(code_str))
            lua_table = self.lua_tool.PrintLuaTable(luaTable, file_name)
            self.print_lua_table(lua_table, file_name)
        except:
            print(full_path)

    def excute_lua_dir(self, full_path):
        all_files = []
        all_dirs = []
        self.root_mapping = {}
        for root, dirs, files in os.walk(full_path):
            for num in range(len(files)):
                file_name = files[num]
                file_full_path = root + "\\" + file_name
                if file_full_path not in all_files and ".lua" in file_full_path:
                    all_files.append(file_full_path)
                dir_head_path = file_full_path.replace(self.input_path, "")
                dir_head_path = dir_head_path.replace(file_name, "")
                dir_head_path = dir_head_path[1:]
                if dir_head_path not in all_dirs:
                    all_dirs.append(dir_head_path)
                self.root_mapping[file_name] = dir_head_path

        for num in range(len(all_dirs)):
            full_ex_path = self.export_path + "\\" + all_dirs[num]
            folder = os.path.exists(full_ex_path)
            if not folder:
                os.makedirs(full_ex_path)

        for num in range(len(all_files)):
            # print(all_files[num])
            self.excute_lua_file(all_files[num])

    def print_lua_table(self, lua_table, file_name):
        if lua_table is None:
            return
        export_path = self.export_path
        parent_name = self.root_mapping[file_name]
        if len(parent_name) != 0:
            export_full_path = export_path + "\\" + parent_name + file_name + ".xlsx"
        else:
            export_full_path = export_path + "\\" + file_name + ".xlsx"
        if os.path.exists(export_full_path):
            os.remove(export_full_path)
        cur_excel = xlsxwriter.Workbook(export_full_path)
        # print("lua table count:"+str(len(lua_table)))
        worksheet = cur_excel.add_worksheet()
        # print(file_name)
        # if file_name == "DialogEntity.lua":
        # print(lua_table)
        for column, subTab in lua_table.items():
            for row, value in subTab.items():
                position = charList[row - 1] + str(column)
                # print(position)
                is_lua_tab = self.lua_tool.IsArrayTable(value)
                if is_lua_tab == 1:
                    worksheet.write(position, self.get_lua_table_data(value))
                else:
                    worksheet.write(position, value)

        cur_excel.close()

    def get_lua_table_data(self, lua_table):
        content = ""
        last_index = len(lua_table)
        for index, value in lua_table.items():
            if last_index == index:
                content += str(value)
            else:
                content += str(value) + ","
        return content


if __name__ == '__main__':
    window = SymbolicateWindow()
    window.DwWindow()