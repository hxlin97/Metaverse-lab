using Assets;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using MathNet.Numerics.LinearAlgebra;
using MathNet.Numerics.LinearAlgebra.Double;
using System;

public class Matrix : MonoBehaviour
{
    // Start is called before the first frame update
    public static GameObject inputObject;
    public static GameObject[] parameters;
    public bool isShake = true;
    float shakeTime = 0f;
    int row = 0;
    int col = 0;
    public static int time_delay = 0;
    public static double arg;
    public static float nextTime = 5.0f;
    public static float nextTime1 = 0.5f;
    public static float nextTime2 = 2.5f;

    private static float rate = 5.0f;
    private static float rate1 = 0.5f;
    private static float rate2 = 2.5f;

    public static Color[] colorSet = {
                                Color.green / 2,    //0,0,0,1
                                Color.magenta / 2,     //0.5,0.5,0.5,1
                                Color.red,      //1,0,0,1
                                Color.blue,     //0,0,1,1
                                Color.green,    //0,1,0,1
                                Color.cyan,     //0,1,1,1
                                Color.yellow,   //1,0.92,0.016,1
                                Color.magenta,  //1,0,1,1
                                new Color((255f/255f), (100f/255f), (255f/255f), (255f/255f)),
                                new Color((50f/255f), (255f/255f), (255f/255f), (0255/255f)),
                                new Color((255f/255f), (0f/255f), (110f/255f), (255f/255f)),
                                new Color((255f/255f), (100f/255f), (110f/255f), (100f/255f))
                        };

    public static int[] colParamsNum = { 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 };

    public static string[] forcedFieldParam = { "charge of H: ", 
                                                "charge of O: ", 
                                                "order of hbond: ",
                                                "epsilon: ",
                                                "sigma: ",
                                                "TIP3P cutoff: ",
                                                "epsilon_H_H: ",
                                                "sigma_H_H: ",
                                                "epsilon_O_H: ",
                                                "sigma_O_H: ",
                                                "epsilon_O_O: ",
                                                "sigma_O_O: "
                                        };

    public static double[,] paramInitValue = {  { +0.5564f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f }, 
                                                { 0f, -1.1128f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f }, 
                                                { 0f, 0f, 8f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f },
                                                { 0f, 0f, 0f, 0.2f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f },
                                                { 0f, 0f, 0f, 0f, 3.1f, 0f, 0f, 0f, 0f, 0f, 0f, 0f },
                                                { 0f, 0f, 0f, 0f, 0f, 10f, 0f, 0f, 0f, 0f, 0f, 0f },
                                                { 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f },
                                                { 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f },
                                                { 0f, 0f, 2f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f }, 
                                                { 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f }, 
                                                { 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0.1852f, 0f },
                                                { 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 0f, 3.15f }
                                            };
    public static double[,] paramFinalValue = new double[12,12];

    public static string[,] paramTexts = new string[12, 12];

    //GameObject targetParam = new GameObject();
    //Transform targetParam1 = new Transform();

    public bool changeJoyStick = false;

    static Color orgrinalColor;

    void Start()
    {
        row = 0;
        col = 0;
        Print2DArray(paramInitValue);
        print("matrix starts");

        InitialColor();

        InitParamTexts();
        print("InitialColor finishes");
        GameObject targetParam = new GameObject();
       // targetParam = FindHighLightParam(targetParam);
        //print(targetParam.GetComponent<param_color>().initColor);
        ToChangeColor();
        
        CorrectMatrix();
        CalMatrixSVD();
    }

    // Update is called once per frame
    void Update()
    {

        //ToChangeColor();

        //++time_delay;

        //UpdateColor();

        //InputJoystick();
        System.Random rnd = new System.Random();
        if (Time.time > nextTime1)
        {
            double t1 = random_turbulence.random_double();
            rate1 = Convert.ToSingle(2 * t1);
            nextTime1 = nextTime1 + rate1;
            ShowChosenParamText();
        }
        
        if (Time.time > nextTime2)
        {

            nextTime2 = nextTime2 + rate2;
            row = rnd.Next(12);
            col = rnd.Next(12);
        }
        if (Time.time>nextTime) 
        {
            nextTime = nextTime + rate;
            UpdateColor();
        }


 //   print("time : " + time_delay);
    }

    void InitParamTexts()
    {
        for (int i = 0; i < 12; ++i) {
            paramTexts[i, 0] = forcedFieldParam[i];
            for (int j = i + 1, k = 1; j < 12; ++j, ++k) {
                paramTexts[i, k] = "correlation between " + forcedFieldParam[i] + " and " + forcedFieldParam[j];
                print("i, j : " + i + " " + j + " =" + paramTexts[i, k]);
            }
        }
    }

    private Color RandomColor()
    {
        float r = UnityEngine.Random.Range(0f, 1f);
        float g = UnityEngine.Random.Range(0f, 1f);
        float b = UnityEngine.Random.Range(0f, 1f);
        Color color = new Color(r,g,b);
        return color;
    }


    void InitialColor()
    {
        GameObject matrix = GameObject.Find("Matrix");
        parameters = new GameObject[matrix.transform.childCount];
        print("InitialColor starts");
        int i = 0;
        foreach (Transform param in matrix.transform)
        {
        //    print("i:" + i);
            parameters[i] = param.gameObject;
            //parameters[i].GetComponent<Renderer>().material.color = RandomColor();
            parameters[i].GetComponent<Renderer>().material.color = colorSet[i];
            parameters[i].AddComponent<param_color>();
            parameters[i].GetComponent<param_color>().initColor = colorSet[i];
            int j = 0;
            foreach (Transform correlation in parameters[i].transform)
            {
                //Color new_color;
                //new_color = Color.white * (float)0.5;
                //new_color.a = 1;
                //new_color.r = (colorSet[i].r + colorSet[j].r) / 2;
                //new_color.g = (colorSet[i].g + colorSet[j].g) / 2;
                //new_color.b = (colorSet[i].b + colorSet[j].b) / 2;
                //new_color.a = (colorSet[i].a + colorSet[j].a) / 2;
                //correlation.GetComponent<Renderer>().material.color = new_color;

                //    correlation.gameObject.AddComponent<param_color>();
                //    correlation.gameObject.
                correlation.GetComponent<Renderer>().material.color = RandomColor();
                ++j;
            }
            ++i;
        }
        orgrinalColor = parameters[0].GetComponent<Renderer>().material.color;
    }


    void UpdateColor()
    {
        GameObject matrix = GameObject.Find("Matrix");
        parameters = new GameObject[matrix.transform.childCount];
     //   print("InitialColor starts");
        int i = 0;
        foreach (Transform param in matrix.transform)
        {
            //    print("i:" + i);
            parameters[i] = param.gameObject;
            parameters[i].GetComponent<Renderer>().material.color = colorSet[i];
            parameters[i].AddComponent<param_color>();
            parameters[i].GetComponent<param_color>().initColor = colorSet[i];
            int j = 0;
            foreach (Transform correlation in parameters[i].transform)
            {
                //Color new_color;
                //double value = paramInitValue[i, j] / 10f;
                //new_color = Color.white - (Color.white + Color.black) * (float)(value * 255f / 255f);
                //correlation.GetComponent<Renderer>().material.color = new_color;
                correlation.GetComponent<Renderer>().material.color = RandomColor();
                ++j;
            }
            ++i;
        }

    }

    GameObject FindHighLightParam(GameObject inputObject)
    {
      //  print("HighlightColor starts");
        
        GameObject highLightParam = new GameObject();
        //  Transform cube;
        if (row == 0)
        {
            parameters[col].GetComponent<Renderer>().material.color = Color.white;
            inputObject = parameters[col];
        }
        else
        {
            int i = 0;
            foreach (Transform cube in parameters[col].transform)
            {
                inputObject = cube.gameObject;
                highLightParam.GetComponent<Renderer>().material.color = Color.white;
                ++i;
                if (i >= row)
                {
                    break;
                }
            }
        }

        print("name: " + inputObject.name);

        changeJoyStick = false;

        return inputObject;
    }

    
    void ToChangeColor()
    {
        inputObject = parameters[col];
        
        if (row == 0)
        {
            inputObject = parameters[col];
        }
        else
        {
            int i = 0;
            foreach (Transform cube in parameters[col].transform)
            {
                inputObject = cube.gameObject;
                orgrinalColor = cube.GetComponent<param_color>().initColor;
                ++i;
                if (i >= row)
                {
                    break;
                }
            }
        }

        if (changeJoyStick == true)
        {
            orgrinalColor = inputObject.GetComponent<Renderer>().material.color;
            print("orgrinalColor = " + orgrinalColor);
            changeJoyStick = false;
        }

        if (isShake)
        {
            shakeTime += Time.deltaTime;
      
            if (shakeTime % 1 > 0.5f)
            {
                inputObject.GetComponent<Renderer>().material.color = orgrinalColor;
            }
            else
            {
                inputObject.GetComponent<Renderer>().material.color = Color.white;
            }
        }

        
    }

    void BackColor()
    {
        GameObject inputObject = parameters[0];

        if (row == 0)
        {
            inputObject = parameters[col];
        }
        else
        {
            int i = 0;
            foreach (Transform cube in parameters[col].transform)
            {
                inputObject = cube.gameObject;
                orgrinalColor = cube.GetComponent<param_color>().initColor;
                ++i;
                if (i >= row)
                {
                    break;
                }
            }
        }

        inputObject.GetComponent<Renderer>().material.color = orgrinalColor;

    }

    void InputJoystick()
    {
        //print("InputJoystick");
        if ((Input.GetAxis("joy_right_y") == 1) && (time_delay > 50))       //down
        {
            print("pressed go down");
            if (row + col >= 11)
            {
                print("Can't go down, please go other side.");
            }
            else
            {
                BackColor();
                ++row;
                changeJoyStick = true;
                //row %= 12 - col;
            }
            time_delay = 0;
        }
        else if ((Input.GetAxis("joy_right_y") == -1) && (time_delay > 50))       //up
        {
            print("pressed go up");
            if (row <= 0)
            {
                print("Can't go right, please go other side.");
            }
            else
            {
                BackColor();
                --row;
                changeJoyStick = true;
            }
            time_delay = 0;
        }
        else if ((Input.GetAxis("joy_right_x") == 1) && (time_delay > 50))       //right
        {
            print("go right");
            if (row <= 0)
            {
                print("Can't go right, please go other side.");
            }
            else
            {
                BackColor();
                ++col;
                --row;
                /*    if (col >= 12)
                    {
                        col = 0;
                        row = 0;
                    }*/
                changeJoyStick = true;
            }

            time_delay = 0;
        }
        else if ((Input.GetAxis("joy_right_x") == -1) && (time_delay > 50))       //left
        {
            print("go left");
            if (col == 0)
            {
                print("Can't go left, please go other side.");
            }
            else
            {
                BackColor();
                --col;
                ++row;
                if (col < 0)
                {
                    col += 12;
                    row = 0;
                }
                changeJoyStick = true;
            }
            time_delay = 0;
        }

    //    print("col = " + col + ", row = " + row);
    }

    void ShowChosenParamText()
    {
        arg = paramInitValue[col, row];
        //arg += Input.GetAxis("joy_left_x") / 1000;
        double t = random_turbulence.random_double();
        arg += (t - 0.5f)/5;
        //GameObject.Find("param_text").GetComponent<Text>().text = " Chosen Parameter: " + paramTexts[col, row];
        GameObject.Find("param_text").GetComponent<Text>().text = "Entry" + "(" + col.ToString() + ", " +row.ToString()+")";
        GameObject.Find("correlation_value").GetComponent<Text>().text = Convert.ToString(arg);
        paramInitValue[col, row] = arg;
    }


    void CorrectMatrix()
    {
    //    Print2DArray(paramInitValue);
        double[,] tmpParamArr = paramInitValue;
    //    Print2DArray(paramInitValue);

        for (int i = 0; i < 12; ++i) {
            for (int j = i; j < 12; ++j) {
                paramFinalValue[i, j] = tmpParamArr[i, j - i];
            }
        }

    //    Print2DArray(paramInitValue);

        for (int i = 0; i < 12; ++i) {
            for (int j = 0; j < i; ++j) {
                paramFinalValue[i, j] = paramFinalValue[j, i];
            }
        }
        //    var D = paramFinalValue;
    //    Print2DArray(paramInitValue);
    //    Print2DArray(paramFinalValue);
    //     print(paramFinalValue);
    //  print(D);
    }


    void CalMatrixSVD()
    {
        var mb = Matrix<double>.Build;
        var A = mb.DenseOfArray(paramFinalValue);
        var S = A.Svd().S;  //一维对角线的值，但是不按顺序
        var U = A.Svd().U;
        var VT = A.Svd().VT;
        var diagonal = A.Svd().S;
       // var diagonal = A.Svd().Determinant;

        print("D:" + diagonal);
     //   print("S:" + S);
     //   print("U:" + U);
     //   print("VT:" + VT);
    }



    void Print2DArray<T>(T[,] matrix)
    {
        string a = "";
        for (int i = 0; i < matrix.GetLength(0); i++)
        {
            for (int j = 0; j < matrix.GetLength(1); j++)
            {
                //   print(matrix[i, j]);
                a += matrix[i, j] + "\t";
                Console.Write(matrix[i, j] + "\t");
            }
            a += "\n";

            Console.WriteLine();
        }
        print(a);
    }


    //显示部分初步完成，需要手柄调试上下左右
    //还没有做如何把参数保存并传出去
    //save.cs的bug
}
