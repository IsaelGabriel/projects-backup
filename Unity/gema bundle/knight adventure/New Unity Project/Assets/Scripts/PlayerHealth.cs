using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;


public class PlayerHealth : MonoBehaviour
{
	public int health;
	public int numOfHearts;

	private Text lText;
	private string displayLives;
	private GameMaster gm;
	public Vector3 spawnpointPosition;

	private float immunityTime;
	public float immunitySec;
	public Rigidbody rb;
	private float damagePositionX;
	private float damagePositionY;
	public float damageImpulseX;
	public float damageImpulseY;
	private float delayTime;
	private int intialLives = 3;
	public int lives = 2;
	private float yVelocity;

	public Image[] hearts;
	public Sprite fullHeart;
	public Sprite emptyHeart;

	void Start()
	{
		gm = GameObject.FindGameObjectWithTag("GM").GetComponent<GameMaster>();
		lText = GameObject.Find("LifeText").GetComponent<Text>();
		transform.position = gm.lastCheckpointPos;
		//if (transform.position != spawnpointPosition)
		if(gm.timesPlayed > 0)
		{
			lives = gm.lastLives - 1;
		}
		else
		{
			lives = intialLives;
		}
		//lText = Text.FindTextWithTag("LifesValue").GetComponent<Text>();
		immunityTime = immunitySec;
	}

	void Update()
	{
		displayLives = lives.ToString();
		yVelocity = rb.velocity.y;
		if (health > numOfHearts)
		{
			health = numOfHearts;
		}

		for (int i = 0; i < hearts.Length; i++) {
			if(i < health)
			{
				hearts[i].sprite = fullHeart;
			}
			else
			{
				hearts[i].sprite = emptyHeart;
			}
			if(i < numOfHearts)
			{
				hearts[i].enabled = true;
			}
			else 
			{
				hearts[i].enabled = false;
			}
		}

		if (immunityTime > 0) 
		{
			immunityTime -= Time.deltaTime;
		}
		if (delayTime > 0)
		{
			delayTime -=Time.deltaTime;
		}

		if (yVelocity > 100.0f)
		{
			Destroy(gameObject);
		}
		string lInter = (lives).ToString();
		lText.text = lInter;
	}

	void OnCollisionEnter(Collision collision)
	{
		if(collision.gameObject.tag == "Obstacle")
		{
			if (collision.transform.position.x > transform.position.x){
				damagePositionX = -1;
			}
			if (collision.transform.position.x <= transform.position.x){
				damagePositionX = 1;
			}
			if (collision.transform.position.y >= transform.position.y){
				damagePositionY = 0;
			}
			if (collision.transform.position.y < transform.position.y){
				damagePositionY = 1;
			}
			if(immunityTime <= 0){
				health = health -1;
				if(damagePositionY == 1) {
					rb.AddForce(new Vector3((damagePositionX * damageImpulseX), damageImpulseY,0), ForceMode.Impulse);
				}
				if (damagePositionY == 0){
					rb.AddForce(new Vector3(((damagePositionX * damageImpulseX) * 2), 0,0), ForceMode.Impulse);
				}
				delayTime = 0.01f;
				Destroy(collision.gameObject);
				if (delayTime <= 0)
				{
					immunityTime = immunitySec;
				}
			}
		}

		if(collision.gameObject.tag == "Recovery")
		{
			health = health + 1;
			Destroy(collision.gameObject);
		}
		if(collision.gameObject.tag == "InstaKill")
		{
			gm.timesPlayed = gm.timesPlayed + 1;
			SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
			//lives = (lives - 1);
		}
	}


}
