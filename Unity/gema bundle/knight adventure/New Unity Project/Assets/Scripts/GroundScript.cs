using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GroundScript : MonoBehaviour
{
	private bool isFalling = false;
	private float downSpeed = 0;
	private float fallDelay = 1.0f;

	void OnTriggerEnter(Collider collider)
	{
		if(collider.gameObject.tag == "Player")
		{
			if(collider.transform.position.y > transform.position.y)
			{
				Invoke("FallFunction", fallDelay);
			}
		}
	}
	void FallFunction ()
	{
		isFalling = true;
		Destroy(gameObject,10);
	}

	void Update()
	{
		var scriptTime = GameObject.Find("TimerText").GetComponent<ChronoText>();
		if (isFalling)
		{
			downSpeed += (Time.deltaTime/10) * scriptTime.speed;
			transform.position=new Vector3(transform.position.x, transform.position.y-downSpeed, transform.position.z);
		}
	}
}
