package com.example.smartwardrobe.rate

import android.content.Context
import android.os.Bundle
import com.google.android.material.snackbar.Snackbar
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.navigateUp
import androidx.navigation.ui.setupActionBarWithNavController
import com.example.smartwardrobe.R
import com.example.smartwardrobe.databinding.ActivityRateBinding

class RateActivity : AppCompatActivity() {

    private lateinit var appBarConfiguration: AppBarConfiguration
    private lateinit var binding: ActivityRateBinding
    lateinit var outfitId: String
    lateinit var userId: String
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityRateBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setSupportActionBar(binding.toolbar)
        outfitId = intent.getStringExtra("outfit_id").toString()
//        userId = intent.getStringExtra("user_id").toString()
        val sharedPreferences = getSharedPreferences("myPrefs", Context.MODE_PRIVATE)
        if (sharedPreferences.contains("name")) {
            userId = sharedPreferences.getString("id", null).toString()
        }

        val navController = findNavController(R.id.nav_host_fragment_content_rate)
        appBarConfiguration = AppBarConfiguration(navController.graph)
        setupActionBarWithNavController(navController, appBarConfiguration)

    }

    override fun onSupportNavigateUp(): Boolean {
        val navController = findNavController(R.id.nav_host_fragment_content_rate)
        return navController.navigateUp(appBarConfiguration)
                || super.onSupportNavigateUp()
    }
}