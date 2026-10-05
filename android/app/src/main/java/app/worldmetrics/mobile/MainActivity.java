package app.worldmetrics.mobile;

import android.content.pm.ActivityInfo;
import android.content.res.Configuration;
import android.os.Bundle;
import android.webkit.JavascriptInterface;

import androidx.activity.OnBackPressedCallback;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    private OnBackPressedCallback worldMetricsBackCallback;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getBridge() != null && getBridge().getWebView() != null) {
            getBridge().getWebView().addJavascriptInterface(new WorldMetricsNativeBridge(), "WorldMetricsNative");
        }
        worldMetricsBackCallback = new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                if (getBridge() == null || getBridge().getWebView() == null) { finish(); return; }
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

    private class WorldMetricsNativeBridge {
        @JavascriptInterface
        public void setOrientation(String orientation) {
            runOnUiThread(() -> {
                if ("landscape".equals(orientation)) setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
                else if ("portrait".equals(orientation)) setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
                else setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED);
            });
        }
        @JavascriptInterface
        public String getOrientation() {
            int value = getResources().getConfiguration().orientation;
            return value == Configuration.ORIENTATION_LANDSCAPE ? "landscape" : "portrait";
        }
    }
}
