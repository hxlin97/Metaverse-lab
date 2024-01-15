using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class bubble_control : MonoBehaviour
{
    ParticleSystem bubble;
    ParticleSystem bubble1;
    ParticleSystem bubble2;
    bool change1 = false;
    bool change2 = false;

    // Start is called before the first frame update
    void Start()
    {
        bubble = GameObject.Find("bubbles").GetComponent<ParticleSystem>();
        var bubble_emission = bubble.emission;
        bubble_emission.enabled = true;
        bubble1 = GameObject.Find("bubbles1").GetComponent<ParticleSystem>();
        var bubble1_emission = bubble1.emission;
        bubble1_emission.enabled = false;
        bubble2 = GameObject.Find("bubbles2").GetComponent<ParticleSystem>();
        var bubble2_emission = bubble2.emission;
        bubble2_emission.enabled = false;

        Debug.Log("bubble initiated");


    }

    // Update is called once per frame
    void Update()
    {
        if (Time.time >= 10 && Time.time <= 20 && change1 == false)
        {
            var bubble_emission = bubble.emission;
            bubble_emission.enabled = false;
            Debug.Log("bubble changed from 1 to 2");
            var bubble1_emission = bubble1.emission;
            bubble1_emission.enabled = true;
            change1 = true;
        }
        if (Time.time >= 20 && change2 == false)
        {
            var bubble1_emission = bubble1.emission;
            bubble1_emission.enabled = false;
            Debug.Log("bubble changed");
            var bubble2_emission = bubble2.emission;
            bubble2_emission.enabled = true;
            change2 = true;
        }
    }
}
