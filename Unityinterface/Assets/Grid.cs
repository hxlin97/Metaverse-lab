using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;

public class Grid : MonoBehaviour
{
    public float gridwidth;
    public float gridheight;
    public Color color;
    public Action Onclick;


    // Update is called once per frame
    void Update()
    {
        gameObject.GetComponent<MeshRenderer>().material.color = color;
    }

    private void OnMouseDown()
    {
        Onclick?.Invoke();
    }
}
