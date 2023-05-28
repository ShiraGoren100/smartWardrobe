package com.example.smartwardrobe

import android.content.Context
import android.os.Bundle
import androidx.preference.Preference
import androidx.preference.PreferenceFragmentCompat

class SettingsFragment : PreferenceFragmentCompat() {
    private lateinit var buttonPreference: Preference


    override fun onCreatePreferences(savedInstanceState: Bundle?, rootKey: String?) {
        setPreferencesFromResource(R.xml.root_preferences, rootKey)


        buttonPreference = findPreference("logoutButton")!!

        // Enable the preference button
        buttonPreference.isEnabled = true
        buttonPreference?.setOnPreferenceClickListener {
            val sharedPreferences = (activity as MainActivity).getSharedPreferences("myPrefs", Context.MODE_PRIVATE)
            if (sharedPreferences.contains("name")) {
                sharedPreferences.edit().clear().apply()
                activity?.finish()
            }
            true
        }
    }
}