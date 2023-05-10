package com.example.smartwardrobe.ui.register

import android.app.Activity
import android.content.Context
import android.content.Intent
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import android.os.Bundle
import androidx.annotation.StringRes
import androidx.appcompat.app.AppCompatActivity
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.EditText
import android.widget.Toast
import com.example.smartwardrobe.MainActivity
import com.example.smartwardrobe.databinding.ActivityRegisterBinding

import com.example.smartwardrobe.R
import com.example.smartwardrobe.ui.login.LoggedInUserView
import com.example.smartwardrobe.ui.login.LoginActivity

class RegisterActivity : AppCompatActivity() {

    private lateinit var registerViewModel: RegisterViewModel
    private lateinit var binding: ActivityRegisterBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityRegisterBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val username = binding.etUsername
        val mail = binding.etMail
        val password = binding.etPassword
        val login = binding.login
        val loading = binding.loading

        registerViewModel = ViewModelProvider(this, RegisterViewModelFactory())
            .get(RegisterViewModel::class.java)

        registerViewModel.registerFormState.observe(this@RegisterActivity, Observer {
            val registerState = it ?: return@Observer

            // disable login button unless both username / password is valid
            login.isEnabled = registerState.isDataValid

            if (registerState.usernameError != null) {
                binding.etUsernameLayout!!.error = getString(registerState.usernameError)
            } else {
                binding.etUsernameLayout!!.error = null
            }
            if (registerState.mailError != null) {
                binding.etMailLayout!!.error = getString(registerState.mailError)
            } else {
                binding.etMailLayout!!.error = null
            }
            if (registerState.passwordError != null) {
                binding.etPasswordLayout!!.error = getString(registerState.passwordError)
            } else {
                binding.etPasswordLayout!!.error = null
            }
        })

        registerViewModel.registerResult.observe(this@RegisterActivity, Observer {
            val loginResult = it ?: return@Observer

            loading.visibility = View.GONE
            if (loginResult.error != null) {
                showLoginFailed(loginResult.error)
            }
            if (loginResult.success != null) {
                updateUiWithUser(loginResult.success)
                setResult(Activity.RESULT_OK)

                //Complete and destroy login activity once successful
                //todo: save user to sharedprefrences
                saveUser(loginResult.success)
                val intent = Intent(this, MainActivity::class.java)
                startActivity(intent)
                finish()
            }
        })

        username?.afterTextChanged {
            registerViewModel.registerDataChanged(
                username?.text.toString(),
                mail?.text.toString(),
                password?.text.toString()
            )
        }

        password?.apply {
            afterTextChanged {
                registerViewModel.registerDataChanged(
                    username?.text.toString(),
                    password.text.toString(),
                    password.text.toString()
                )
            }

            setOnEditorActionListener { _, actionId, _ ->
                when (actionId) {
                    EditorInfo.IME_ACTION_DONE ->
                        registerViewModel.register(
                            username?.text.toString(),
                            mail?.text.toString(),
                            password?.text.toString()
                        )
                }
                false
            }

            login.setOnClickListener {
                loading.visibility = View.VISIBLE
                registerViewModel.register(username?.text.toString(), mail?.text.toString(), password.text.toString())
            }
        }

        binding.activityLink!!.setOnClickListener {
            try {
                val intent = Intent(applicationContext, LoginActivity::class.java)
                startActivity(intent)
                finish()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
    private fun saveUser(user: LoggedInUserView?) {
        val sharedPreferences = getSharedPreferences("myPrefs", Context.MODE_PRIVATE)
        val editor = sharedPreferences.edit()

        editor.putString("name", user?.displayName)
        editor.putString("id", user?.id)
        editor.apply()
    }

    private fun updateUiWithUser(model: LoggedInUserView) {
        val welcome = getString(R.string.welcome)
        val displayName = model.displayName
        // TODO : initiate successful logged in experience
        Toast.makeText(
            applicationContext,
            "$welcome $displayName",
            Toast.LENGTH_LONG
        ).show()
    }

    private fun showLoginFailed(@StringRes errorString: Int) {
        Toast.makeText(applicationContext, errorString, Toast.LENGTH_SHORT).show()
    }


    /**
     * Extension function to simplify setting an afterTextChanged action to EditText components.
     */
    fun EditText.afterTextChanged(afterTextChanged: (String) -> Unit) {
        this.addTextChangedListener(object : TextWatcher {
            override fun afterTextChanged(editable: Editable?) {
                afterTextChanged.invoke(editable.toString())
            }

            override fun beforeTextChanged(s: CharSequence, start: Int, count: Int, after: Int) {}

            override fun onTextChanged(s: CharSequence, start: Int, before: Int, count: Int) {}
        })
    }
}