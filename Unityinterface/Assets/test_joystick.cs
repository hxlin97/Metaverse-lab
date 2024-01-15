using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class test_joystick : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        for (int i = 0; i < 4; i++)
        {
            if (Mathf.Abs(Input.GetAxis("JOY" + i + "X")) > 0.2 ||
                Mathf.Abs(Input.GetAxis("JOY" + i + "Y")) > 0.2)
            {
                Debug.Log(Input.GetJoystickNames()[i] + "is moved");
            }
        }
    }
}
