using LiquidVolumeFX;
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class random_turbulence : MonoBehaviour
{

    private float turbulence1_lo = 0;
    private float turbulence1_hi = 0.3f;
    private float turbulence2_lo = 0;
    private float turbulence2_hi = 0.3f;
    private float nextTime = 0;
    private float rate = 0.1f;

    public static double random_double()
    {
        System.Random rand = new System.Random(Guid.NewGuid().GetHashCode());
        double t = rand.NextDouble();
        return t;
    }


    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (Time.time > nextTime) {
            nextTime = nextTime + rate;
            double t1 = random_double();
            double t2 = random_double();
            GameObject.Find("CylinderFlask").GetComponent<LiquidVolume>().turbulence1 = (float)((1 - t1) * turbulence1_lo + t1 * turbulence1_hi);
            GameObject.Find("CylinderFlask").GetComponent<LiquidVolume>().turbulence2 = (float)((1 - t2) * turbulence2_lo + t2 * turbulence2_hi);
        }
        

    }
}
