package app.worldmetrics.mobile;

import android.os.Bundle;

import androidx.activity.OnBackPressedCallback;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    // Device QA v1: native Back delegates to the web UI state before allowing root exit.
    private OnBackPressedCallback worldMetricsBackCallback;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        worldMetricsBackCallback = new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                if (getBridge() == null || getBridge().getWebView() == null) {
                    finish();
                    return;
                }

                getBridge().getWebView().evaluateJavascript(
                    "(function(){try{return !!(window.__worldMetricsHandleBack && window.__worldMetricsHandleBack());}catch(e){return false;}})();",
                    result -> {
                        if (!"true".equals(result)) {
                            setEnabled(false);
                            getOnBackPressedDispatcher().onBackPressed();
                            setEnabled(true);
                        }
                    }
                );
            }
        };

        getOnBackPressedDispatcher().addCallback(this, worldMetricsBackCallback);
    }
}
