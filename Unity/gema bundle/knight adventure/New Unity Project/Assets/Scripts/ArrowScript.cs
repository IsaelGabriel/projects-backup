using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ArrowScript : MonoBehaviour
{
	private bool isMoving = false;
	private float goSpeed = 0;
	//private float destroyDelay = 9.0f;

	void Start()
	{
		Invoke("GoFunction", 2f);

	}
	void GoFunction ()
	{
		isMoving = true;
		Destroy(gameObject,2f);
	}

	void Update()
	{
		if(transform.localScale.x < transform.localScale.y)
		{
			if(transform.rotation.eulerAngles.z != 90)
			{
				transform.Rotate(0,0,90,Space.Self);
			}
		}
		var scriptTime = GameObject.Find("TimerText").GetComponent<ChronoText>();
		if (isMoving)
		{
			goSpeed += (scriptTime.theTime)/10;
			transform.position=new Vector3(transform.position.x-goSpeed, transform.position.y, transform.position.z);
		}
	}
}
