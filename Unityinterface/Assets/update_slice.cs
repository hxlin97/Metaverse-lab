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

        GameObject container = GameObject.Find("container");                    // �ҵ�ģ�ʹ������
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
        //��ʼд��
        sw.Write(cmd_py);
        //��ջ�����
        sw.Flush();
        //�ر���
        sw.Close();
        fs.Close();

        // 2.��Ϊ����������python��дdata�ж�Ӧ�ķ�������
        Process p = new Process();
        p.StartInfo.FileName = CmdPath;
        p.StartInfo.Arguments = @"D:";                  //ָ����ʽ������
        p.StartInfo.UseShellExecute = false;            //�Ƿ�ʹ�ò���ϵͳshell����
        p.StartInfo.RedirectStandardInput = true;       //�������Ե��ó����������Ϣ
        p.StartInfo.RedirectStandardOutput = false;     //�ɵ��ó����ȡ�����Ϣ
        p.StartInfo.RedirectStandardError = false;      //�ض����׼�������
        p.StartInfo.CreateNoWindow = false;

        p.Start();//��������
        p.StandardInput.WriteLine(@"D:");
        p.StandardInput.WriteLine("cd " + Application.dataPath + "/slides/");
        p.StandardInput.WriteLine("python edit_data.py");

        Thread.Sleep(3000);

    }

}
