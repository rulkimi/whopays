import { useEffect, useState } from "react";

type Viewport = {
	isMobile: boolean;
	isTablet: boolean;
	isDesktop: boolean;
	isLargeScreen: boolean;
	width: number;
};

function getViewport(): Viewport {
	if (typeof window === "undefined") {
		return {
			isMobile: false,
			isTablet: false,
			isDesktop: false,
			isLargeScreen: false,
			width: 0,
		};
	}
	const width = window.innerWidth;
	return {
		isMobile: width < 768,
		isTablet: width >= 768 && width < 1024,
		isDesktop: width >= 1024 && width < 1280,
		isLargeScreen: width >= 1280,
		width,
	};
}

export function useViewport(): Viewport {
	const [viewport, setViewport] = useState<Viewport>(getViewport());

	useEffect(() => {
		function handleResize() {
			setViewport(getViewport());
		}
		window.addEventListener("resize", handleResize);
		return () => window.removeEventListener("resize", handleResize);
	}, []);

	return viewport;
}
