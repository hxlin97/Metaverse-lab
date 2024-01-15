using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Threading;
using System.Diagnostics;
using UnityEngine;

public class update_slice : MonoBehaviour
{
    public static string CmdPath;
    
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void UpdateDataFile()
    {
        string cmd_py = "";

        GameObject container = GameObject.Find("container");                    // 找到模型存放容器
        GameObject[] kids = new GameObject[container.transform.childCount];
        float elem_x, elem_y, elem_z;
        string elem_type;

        int elem_id = 0;
        foreach (Transform kid in container.transform)
        {
            kids[elem_id] = kid.gameObject;
            elem_id += 1;
        }
        elem_id = 0;

        foreach (GameObject kid in kids)
        {
            string atom_name = kid.name;
            string[] atom_strs = atom_name.Split(' ');

            ++elem_id;
            elem_x = kid.gameObject.transform.position.x;
            elem_y = kid.gameObject.transform.position.y;
            elem_z = kid.gameObject.transform.position.z;
            elem_type = atom_strs[2];
            cmd_py += elem_id + " " + elem_type + " " + elem_x + " " + elem_y + " " + elem_z + "\n";
            print(kid.gameObject.transform.name + " " + elem_type + " " + elem_x + " " + elem_y + " " + elem_z);
            DestroyImmediate(kid.gameObject);
        }

        FileStream fs = new FileStream(Application.dataPath + "/slides/data_modified.txt", FileMode.Create);
        StreamWriter sw = new StreamWriter(fs);
        //开始写入
        sw.Write(cmd_py);
        //清空缓冲区
        sw.Flush();
        //关闭流
        sw.Close();
        fs.Close();

        // 2.作为参数，调用python改写data中对应的分子坐标
        Process p = new Process();
        p.StartInfo.FileName = CmdPath;
        p.StartInfo.Arguments = @"D:";                  //指定程式命令行
        p.StartInfo.UseShellExecute = false;            //是否使用操作系统shell启动
        p.StartInfo.RedirectStandardInput = true;       //接受来自调用程序的输入信息
        p.StartInfo.RedirectStandardOutput = false;     //由调用程序获取输出信息
        p.StartInfo.RedirectStandardError = false;      //重定向标准错误输出
        p.StartInfo.CreateNoWindow = false;

        p.Start();//启动程序
        p.StandardInput.WriteLine(@"D:");
        p.StandardInput.WriteLine("cd " + Application.dataPath + "/slides/");
        p.StandardInput.WriteLine("python edit_data.py");

        Thread.Sleep(3000);

    }

}
