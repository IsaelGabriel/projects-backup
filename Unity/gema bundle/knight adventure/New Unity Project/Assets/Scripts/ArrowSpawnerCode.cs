using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ArrowSpawnerCode : MonoBehaviour
{
	private bool isCharging = false;
	private float creationDelay = 5.0f;
	public GameObject theArrowObject;

	void Start()
	{
		Invoke("ThisFunction", 5.0f);
	}
	void ThisFunction ()
	{
		isCharging = true;
		creationDelay = 5.0f;
	}

	void Update()
	{
		var scriptTime = GameObject.Find("TimerText").GetComponent<ChronoText>();
		if (!isCharging)
		{
			Invoke("ThisFunction", 0f);
		}
		if (creationDelay > 0)
		{
			creationDelay -= scriptTime.theTime;
		}
		if ((creationDelay < 0)||(creationDelay == 0))
		{
			isCharging = false;
		}
	}

}
