using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PlayerMove : MonoBehaviour
{	
	private Text elixirTxt;
	private int elixirNum = 0;
	private bool elixirActive = false;
	private float elixirDelay = 0f;
	private Light blueLight;

	public float jumpForce = 5f;
	public Rigidbody rb;
	public float speed;
	public float intialSpeed = 10f;
	private bool inGround = true;
    // Start is called before the first frame update
    void Start()
    {
		elixirTxt = GameObject.Find("ElixirText").GetComponent<Text>();
		rb = GetComponent<Rigidbody>();
		blueLight = GetComponent<Light>();
		blueLight.enabled = false;
    }

    // Update is called once per frame
    void Update()
    {
		//transforma o valor do float no valor do comando
		float horizontal = Input.GetAxis("Horizontal") * Time.deltaTime * speed;

		//muda a posicao de acordo com os valores x, y e z
		transform.Translate(horizontal, 0, 0);
		if(Input.GetButtonDown("Fire3"))
		{
			if(!elixirActive)
			{
				if(elixirNum > 0)
				{
					elixirNum = elixirNum - 1;
					speed = speed * 1.7f;
					//particula(tenho que adicionar)
					elixirDelay = 5f;
					elixirActive = true;
				}
			}
		}
		if (elixirActive)
		{
			if(elixirDelay <= 0)
			{
				speed = intialSpeed;
				elixirActive = false;
				blueLight.enabled = false;
			}
		}
		//checa se o botao de pulo foi pressionado e se o player esta no chao
		if(Input.GetButtonDown("Jump") && inGround)
		{
			//adiciona a forca do pulo
			rb.AddForce(new Vector3(0, jumpForce, 0), ForceMode.Impulse);
			//diz que o player saiu do chao
			inGround = false;
		}
		string elixirCount = elixirNum.ToString();
		elixirTxt.text = elixirCount;
		if(elixirDelay > 0f)
		{
			elixirActive = true;
			elixirDelay -= Time.deltaTime;
			blueLight.enabled = true;
		}
	}

	//ativado quando o player entra em colisao
	private void OnCollisionEnter(Collision collision)
	{
		//checa se o player esta em colisao com algum objeto do chao
		if(collision.gameObject.tag == "Ground")
		{
			//diz que o player esta no chao
			inGround = true;
		}
		if(collision.gameObject.tag == "PowerUp")
		{
			elixirNum = elixirNum+1;
			Destroy(collision.gameObject);
		}
	}
	private void OnColissionExit(Collision collision)
	{
		if(collision.gameObject.tag == "Ground")
		{
			inGround = false;
		}
	}
}
