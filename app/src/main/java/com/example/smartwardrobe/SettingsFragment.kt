package com.example.smartwardrobe

import android.content.ContentValues.TAG
import android.content.Context
import android.os.Bundle
import android.util.Log
import androidx.lifecycle.lifecycleScope
import androidx.preference.EditTextPreference
import androidx.preference.Preference
import androidx.preference.PreferenceFragmentCompat
import com.google.android.material.snackbar.Snackbar
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import kotlin.math.log

class SettingsFragment : PreferenceFragmentCompat() {
    private lateinit var buttonPreference: Preference
    private lateinit var intervalPreference: EditTextPreference


    override fun onCreatePreferences(savedInstanceState: Bundle?, rootKey: String?) {
        setPreferencesFromResource(R.xml.root_preferences, rootKey)
        buttonPreference = findPreference("logoutButton")!!

        // Enable the preference button
        buttonPreference.isEnabled = true
        val sharedPreferences = (activity as MainActivity).getSharedPreferences("myPrefs", Context.MODE_PRIVATE)
        buttonPreference?.setOnPreferenceClickListener {
            if (sharedPreferences.contains("name")) {
                sharedPreferences.edit().clear().apply()
                activity?.finish()
            }
            true
        }

        intervalPreference = findPreference("interval")!!

        if (sharedPreferences.contains("name")) {
            intervalPreference?.text = sharedPreferences.getString("interval", null).toString()
        }

        intervalPreference.setOnPreferenceChangeListener { preference, newValue ->
            //todo: call function to update interval
            val newInterval = newValue.toString().toInt() // Assuming the new value is an integer
            updateInterval(newInterval)
            val editor = sharedPreferences.edit()
            editor.putString("interval", newValue.toString())
            editor.apply()
            true
        }
    }

    private fun updateInterval(newInterval: Int) {
        val retrofit = RetrofitClient.myApi

        // Create the request body with the new interval value
        val queryParameters = mapOf("id" to (activity as MainActivity).userid, "interval" to newInterval.toString())

        val call = retrofit.updateInterval(queryParameters)
        call.enqueue(object : Callback<ResponseBody> {
            override fun onResponse(call: Call<ResponseBody>, response: Response<ResponseBody>) {
                // handle successful response
//                callback.onSuccess()
                Log.i(TAG, "onResponse: success")
            }

            override fun onFailure(call: Call<ResponseBody>, t: Throwable) {
                // handle error
//                callback.onError("Error message")
                Log.e(TAG, "onFailure: ", t.cause)
            }
        })

    }

}