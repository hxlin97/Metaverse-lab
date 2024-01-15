//namespace VRTK
//{
using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;
using LiquidVolumeFX;

public class changecolor : MonoBehaviour
{
    //static bool istogon=false;
    //Transform changer;
    //public GameObject originobj; 
    private Color origin = new Color(1,1,1,0.1f);
    //private Color end = new Color32(229,12,221,255);
    private Color end = new Color32(10, 120,200,255);
    private Color mid = new Color32(10, 120, 255, 255);
    private float duration = 30;
    private float duration1 = 150;
    private float timer;
    public GameObject glass;

    public void Toggle(bool state)
    {
        //Debug.Log("The toggle state is " + (state ? "on" : "off"));
        //changer = transform.Find("container");
        ////Color origin = changer.GetChild(0).GetComponent<MeshRenderer>().material.color;
        //print(changer.name);
        //istogon = state;
        //print(istogon);

    }

    void change()
    {
        float lerp1 = Mathf.PingPong(Time.time, duration) / duration;
        float lerp2 = Mathf.PingPong(Time.time, duration1) / duration1;
        if (Time.time < duration) 
        {
            glass.GetComponent<LiquidVolume>().liquidColor1 = Color.Lerp(origin, mid, lerp1);
        }
        else
        {
            glass.GetComponent<LiquidVolume>().liquidColor1 = Color.Lerp(mid, end, lerp2);
        }
        
        //glass.GetComponent<LiquidVolume>().liquidColor1 = mid;

    }


    void Start()
    {
        //glass = GameObject.Find("Potion");
        //glass.GetComponent<LiquidVolume>().emissionColor = origin;
        //glass.GetComponent<LiquidVolume>().liquidColor1 = origin;
        //glass.GetComponent<LiquidVolume>().emissionBrightness = 0f;
        // print(origin);
        // print(this.name);
        // print(originobj.name);
        //base.Start();
        //changer = transform.Find("container");
        ////Color origin = changer.GetChild(0).GetComponent<MeshRenderer>().material.color;
        //print(changer.name);
        //print(origin);
    }

    void Update()
    {
        //print(this.GetComponent<MeshRenderer>().material.color);
        //if(istogon==true)
        //{
        //    if (this.GetComponent<Text>().text == "0")
        //    {
        //        this.GetComponent<MeshRenderer>().material.color = new Color(0.5f, 0.5f, 0.1f, 1f);
        //    }
        //    else if (this.GetComponent<Text>().text == "1")
        //    {
        //        this.GetComponent<MeshRenderer>().material.color = new Color(1f, 0.6f, 0f, 1f);
        //    }
        //    else if (this.GetComponent<Text>().text == "2")
        //    {
        //        this.GetComponent<MeshRenderer>().material.color = new Color(0f, 0f, 0.6f, 1f);
        //    }
        //    else if (this.GetComponent<Text>().text == "3")
        //    {
        //        this.GetComponent<MeshRenderer>().material.color = new Color(1f, 0.1f, 0f, 1f);
        //    }
        //    else if (this.GetComponent<Text>().text == "4")
        //    {
        //        this.GetComponent<MeshRenderer>().material.color = new Color(0f, 0.6f, 0f, 1f);
        //    }

        //    print(this.GetComponent<Text>().text);
        //print(origin);
        //print(a);

        //this.GetComponent<MeshRenderer>().material.color = new Color(i * Time.deltaTime, 0f, 0f, 1f);
        //i++;
        //if (i > 60)
        //{
        //    i = 1;
        //}
        //print(this.GetComponent<MeshRenderer>().material.color);

        //}
        //if(istogon==false)
        //{
        //    this.GetComponent<MeshRenderer>().material.color = origin;
        //    //print(a);
        //}
        timer += Time.deltaTime;
        if (timer <= duration1)
        {
            change();
        }



    }

}
//}
