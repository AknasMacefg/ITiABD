package com.example.maslov_an_id_23_1_pr3;

import android.graphics.Typeface;
import android.os.Bundle;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.style.StyleSpan;
import android.widget.GridView;
import android.widget.TextView;
import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        onLoad();
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }

    void onLoad() {
        TextView nameText = findViewById(R.id.name);
        TextView ageText = findViewById(R.id.age);
        TextView courseText = findViewById(R.id.course);
        nameText.setText(getBoldAfterColon("Имя: Александр"));
        ageText.setText(getBoldAfterColon("Возраст: 23"));
        courseText.setText(getBoldAfterColon("Профиль: Мобильная разработка"));
        GridView gridShow = findViewById(R.id.gridShow);
        int[] images = {
                R.drawable.apple,
                R.drawable.apple,
                R.drawable.apple,
                R.drawable.apple
        };
        ImageAdapter adapter = new ImageAdapter(this, images);
        gridShow.setAdapter(adapter);
    }
    private SpannableString getBoldAfterColon(String text) {
        SpannableString spannable = new SpannableString(text);
        int colonIndex = text.indexOf(":");
        if (colonIndex != -1 && colonIndex < text.length() - 1) {
            spannable.setSpan(
                    new StyleSpan(Typeface.BOLD),
                    colonIndex + 1,
                    text.length(),
                    Spanned.SPAN_EXCLUSIVE_EXCLUSIVE
            );
        }
        return spannable;
    }
}
