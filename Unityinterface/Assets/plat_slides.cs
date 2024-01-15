using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using UnityEngine.UI;
using System.IO;
using System.Threading;
using UnityEngine.EventSystems;
using VRTK;
using Assets;

public class plat_slides : MonoBehaviour
{
    public static int visualization_frame;                                  // the frame to show
    public static string result_file;
    public static string[] map_row_string;
    private static int atomnum = 4768;
    private static int framenum = 1000;
    //private int atomnum = 5473;
    //private int framenum = 401;
    //private int frame = 1;
    public static int map_row_max_cells;
    public static List<List<string>> map_Collections = new List<List<string>>();

    private static float nextTime = 5.0f;
    private static float rate = 0.35f;
    public void visualization()
    {

        GameObject container = GameObject.Find("container");                // 找到模型存放容器
        GameObject[] kids = new GameObject[container.transform.childCount];

        int j = 0;
        foreach (Transform kid in container.transform)
        {
            kids[j] = kid.gameObject;
            j += 1;
        }
        foreach (GameObject kid in kids)
        {
            DestroyImmediate(kid.gameObject);
        }                                                                   // clean up the container
        map_Collections.Clear();


        for (int i = (visualization_frame) * (atomnum + 1) + 1; i < (visualization_frame ) * (atomnum + 1)+1+atomnum; i++)       //读取每一行的数据
        {
            //print("slicing a row now.");
            //print("Now at row number " + i.ToString());
            List<string> map_row = new List<string>(map_row_string[i].Split(' '));//按空格分割每个一个单元格
            //print("row sliced.");
            if (map_row_max_cells < map_row.Count)
            {//求一行中最多有个单元格
                map_row_max_cells = map_row.Count;
            }
            map_Collections.Add(map_row);//整理好，放到容器map_Collections中
            //print("reading line " + i.ToString());

        }
        //print("Dump data read.");

        

        //if (isupdate == false)
        for (int i = 0; i < map_Collections.Count; i++)//Z方向是长度就是容器的大小，也就是*读入数据*有多少有效的行
        {
            GameObject atom = Resources.Load("Prefabs/Au") as GameObject;
            GameObject atomInstance = Instantiate(atom);
            //print("before bug?");
            atomInstance.transform.parent = container.transform;
            //print("after bug?");

            atomInstance.name = "sphere " + i;
            //print("atom named with number " + i);
            atomInstance.transform.position = new Vector3(float.Parse(map_Collections[i][4])/8f+12,
                                                          float.Parse(map_Collections[i][2])/8f+1,
                                                          float.Parse(map_Collections[i][3])/8f+2);
            //print("atom repositioned");

            float element_type = float.Parse(map_Collections[i][1]);
            if (element_type == 1)
            {
                atomInstance.GetComponent<Renderer>().material.color = Color.white;
                atomInstance.transform.localScale = new Vector3(0.1f, 0.1f, 0.1f);
            }
            else if (element_type == 2)
            {
                atomInstance.GetComponent<Renderer>().material.color = Color.grey;
                atomInstance.transform.localScale = new Vector3(0.18f, 0.18f, 0.18f);
            }
            else if (element_type == 3)
            {
                atomInstance.GetComponent<Renderer>().material.color = Color.blue;
                atomInstance.transform.localScale = new Vector3(0.24f, 0.24f, 0.24f);
            }
            else if (element_type == 4)
            {
                atomInstance.GetComponent<Renderer>().material.color = Color.green;
                atomInstance.transform.localScale = new Vector3(0.2f, 0.2f, 0.2f);
            }
            //atom.GetComponent<Text>().text = map_Collections[i][5];
        }
    }
    // Start is called before the first frame update
    void Start()
    {
        visualization_frame = 0;
        //result_file = "CuSO4_slides.trj";
        result_file = "slides.trj";
        map_row_string = File.ReadAllLines(Application.dataPath + "/slides/" + result_file);
       
        //atomnum = int.Parse(map_row_string[1]);                               
        //framenum = int.Parse(map_row_string[0]);                                     
        map_row_max_cells = 5;
        //visualization();

    }

    // Update is called once per frame
    void Update()
    {
        //if (Input.GetKeyUp(KeyCode.K)) 
        //{
        //    visualization_frame += 1;
        //    visualization();

        //}

        if (Time.time>nextTime)
        {
            nextTime = nextTime + rate;
            visualization();
            visualization_frame += 1;
        }
        
    }
}
